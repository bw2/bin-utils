#!/usr/bin/env python3

"""
vt normalize has these errors:

[variant_manip.cpp:96 is_not_ref_consistent] reference bases not consistent: chr12:111598949-111599018  GCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTG(REF) vs GCTGCTGCTGCTGCTGCTGCTGCTGCTGTTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTG(FASTA)
[normalize.cpp:209 normalize] Normalization not performed due to inconsistent reference sequences. (use -n or -m option to relax this)

The vt normalize -n -m options don't work, so just replace the string
"""

import argparse
import pyfaidx
import sys

from utils.fasta_utils import get_reference_sequence

def parse_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument("fasta_path", help="reference fasta path")

    return p.parse_args()


def main():
    args = parse_args()

    fasta_obj = pyfaidx.Fasta(args.fasta_path, one_based_attributes=False, as_raw=True)

    for line in sys.stdin:
        if line.startswith("#"):
            sys.stdout.write(line)
            continue

        fields = line.rstrip("\n").split("\t")

        chrom = fields[0]
        pos = int(fields[1])
        id_field = fields[2]
        ref = fields[3].upper()

        if chrom not in fasta_obj:
            if "chr" in chrom:
                fixed_chrom = chrom.replace("chr", "")
            else:
                fixed_chrom = "chr" + chrom

            if fixed_chrom in fasta_obj:
                chrom = fixed_chrom

        actual_ref = get_reference_sequence(fasta_obj, chrom, pos, pos + len(ref))
        if actual_ref is None:
            actual_ref = ref

        other_fields = fields[4:]

        sys.stdout.write("\t".join([chrom, str(pos), id_field, actual_ref] + other_fields) + "\n")

        """
        if len(ref) < 20:
            actual_ref = get_reference_sequence(fasta_obj, chrom, pos, pos + len(ref))
            if actual_ref is None:
                actual_ref = ref

        else:
            # GangSTR ref allele is sometimes off by one from the reference position. If so, shift the
            # position so that the ref allele matches the reference.
            for offset in [0, -1, 1, -2, 2]:
                actual_ref_at_offset = get_reference_sequence(fasta_obj, chrom, pos + offset, pos + offset + len(ref))
                if actual_ref_at_offset == ref:
                    #sys.stderr.write(f"-- {chrom} {pos}: Shifting pos by {offset} \n" )
                    pos = pos + offset
                    actual_ref = ref
                    break
            else:
                actual_ref = get_reference_sequence(fasta_obj, chrom, pos, pos + len(ref))
                if actual_ref is None:
                    actual_ref = ref

        other_fields = fields[4:]

        sys.stdout.write("\t".join([chrom, str(pos), id_field, actual_ref] + other_fields) + "\n")
        """

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import collections
import datetime
from dateutil import parser
import gzip
import os
import pytz
import re
import subprocess
import tqdm

p = argparse.ArgumentParser(description="This script takes a Google Storage bucket path (eg. gs://my-bucket or gs://my-bucket/dir/) and "
                            "runs 'gsutil ls' to get all files and subdirectories as well as their sizes and last-modified dates. Then it "
                            "prints all files and subdirectories larger than a user-specified threshold (default 100Gb)")
p.add_argument("--overwrite", help="Rerun 'gsutil ls' to get all files even if the cached results file already exists in the current directory", action="store_true")
p.add_argument("-t", "--threshold", type=int, help="Print paths larger than this many gigabytes (default: 10)", default=10)
p.add_argument("-p", "--requester-pays-project", help="Google Cloud project to use for requester-pays buckets")
p.add_argument("--sort-by", help="Sort output by size or by date", choices=("date", "size"), default="size")
p.add_argument("bucket_path", help="Bucket path (eg. gs://gnomad-bw2/) to check for file sizes")
args = p.parse_args()

# Run gsutil ls to get all files under bucket_path
output_filename = re.sub("^gs://", "", args.bucket_path).strip("/").replace("/", "_") + ".file_sizes.txt.gz"

print(f"Writing to {output_filename}")

def run(cmd):
    print(cmd)
    result = subprocess.check_output(cmd, shell=True)
    return result

if not os.path.isfile(output_filename) or args.overwrite:
    cmd = "gsutil"
    if args.requester_pays_project:
       cmd += f" -u {args.requester_pays_project}"
    run(f"{cmd} ls -l {os.path.join(args.bucket_path, '**')} | gzip -c - > {output_filename}")


"""
Example:
     99915  2021-11-28T21:54:25Z  gs://gnomad-bw2/strling/Homo_sapiens_assembly38.fasta.str
  30614755  2020-10-18T22:50:13Z  gs://gnomad-bw2/test/test.bam
     38937  2020-09-10T08:44:57Z  gs://gnomad-bw2/v3_1_sample_ids.txt
TOTAL: 3531206 objects, 4492616987222 bytes (4.09 TiB)
"""

# Parse results
print(f"Parsing {output_filename}")
txt_file_size = run(f"gunzip -c {output_filename} | wc -l")
txt_file_size = int(txt_file_size.strip())

total_size_line = None
path_is_dir = {}
path_to_total_size = collections.defaultdict(int)
path_to_total_objects = collections.defaultdict(int)
path_to_latest_date = collections.defaultdict(lambda: datetime.datetime(1,1,1, tzinfo=pytz.UTC))

file_obj = gzip.open(output_filename, "rt")
for line in tqdm.tqdm(file_obj, total=txt_file_size, unit=" lines"):
    line = line.strip()    
    if line.startswith("TOTAL:"):
        total_size_line = line
        #match = re.search("TOTAL: ([0-9]+) objects, ([0-9]+) bytes", line)
        #if match:
        #    total_size = int(match.group(2))
        #    total_objects = int(match.group(1))
    else:
        try:
            size_string, date_string, file_path = line.split("  ")
        except Exception as e:
            print(f"WARNING: Unable to parse line: {line}   {e}")
            continue
        path_size = int(size_string)
        path_date = parser.parse(date_string)
        path = re.sub("^gs://", "", file_path).strip("/")

        is_dir = False
        while len(path) > 1:
            path_is_dir[path] = is_dir
            path_to_total_objects[path] += 1
            path_to_total_size[path] += path_size
            if path_to_latest_date[path] < path_date:
                path_to_latest_date[path] = path_date
            path = os.path.dirname(path)
            is_dir = True

# Print results 
if args.sort_by == "size":
    sort_by_func = lambda path: -path_to_total_size[path]
elif args.sort_by == "date":
    sort_by_func = lambda path: path_to_latest_date[path]
else:
    p.error(f"Unexpected args.sort_by value: {args.sort_by}")

for is_dir, label in [(False, "Files"), (True, "Directories")]:
    print(f"{label} >= {args.threshold} Gb:")
    for path in sorted(path_to_total_size, key=sort_by_func):
        path_size = path_to_total_size[path]
        if path_size < args.threshold * 10**9:
            continue
        if path_is_dir[path] != is_dir:
            continue
        path_size /= 10**9
        date_string = str(path_to_latest_date[path]).split("+")[0]
        total_objects = path_to_total_objects[path]
        if is_dir:
            print(f" {path_size:10.1f} Gb   (last modified: {date_string})  {total_objects:12d} files   gs://{path}")
        else:
            print(f" {path_size:10.1f} Gb   (last modified: {date_string})     gs://{path}")
    print("")
    
if total_size_line is None:
    print(f"WARNING: 'TOTAL: ' line not found at the end of {output_filename}. gsutil ls command may not have completed successfully.")
else:
    print(f"gsutil reported {total_size_line}")
    

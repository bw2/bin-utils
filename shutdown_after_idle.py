#!/usr/bin/env python3
import argparse
import logging
import re
import subprocess
import time

logging.basicConfig(level="INFO", format='%(asctime)-15s %(levelname)s: %(message)s')

p = argparse.ArgumentParser(
    description="Run this script on a machine in the background to shutdown the machine when load stays below some threshold for some number of mintues", 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
p.add_argument("-L", "--load-threshold", type=float, default=0.2, help="utpime load below this threshold will be considered idle")
p.add_argument("--minutes", type=float, default=60, help="shutdown after idle for this many minutes")
args = p.parse_args()

idle_minutes_counter = 0
logging.info("This machine will shutdown if load stays <= {} for {} minutes...".format(args.load_threshold, args.minutes))

SLEEP_SECONDS = 6
while idle_minutes_counter < args.minutes:
    time.sleep(SLEEP_SECONDS)
    uptime_output = subprocess.check_output(["uptime"], encoding="UTF-8")
    logging.debug(uptime_output)

    match = re.search("load average: ([0-9]+.[0-9]+)", uptime_output)
    if not match:
        logging.error("Unable to parse uptime output: {}".format(uptime_output))
    current_load = float(match.group(1))

    if current_load <= args.load_threshold:
        idle_minutes_counter += SLEEP_SECONDS/60.0
        logging.info("Current load = {}. This machine will shutdown if load stays <= {} for {:0.1f} more minutes.".format(
                current_load, args.load_threshold, args.minutes - idle_minutes_counter))
    else:
        logging.info("Current load = {}. Idle time reset to 0.".format(current_load))
        idle_minutes_counter = 0

logging.info("Shutting down...")
command = ["sudo", "powerdown"]

#subprocess.check_output(command)

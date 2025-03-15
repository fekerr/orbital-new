#!/usr/bin/env python3
"""
check_yaml.py

This script checks a YAML file using yamllint and writes the output
to a log file in the "logs" directory. The file is named based on the
base name of the YAML file, today's date in YYYYMMDD format, and an
incrementing counter (e.g., output_2d_chunks_20250315_001.log).

Usage:
    python3 check_yaml.py <filename>

It respects the environment variable FEKERR_YAML_CHECK:
  - If FEKERR_YAML_CHECK is "1" (default), yamllint runs.
  - If FEKERR_YAML_CHECK is "0", linting is skipped.
"""

import os
import sys
import glob
import datetime
import subprocess

def get_log_filename(file_path):
    """Generate a log filename using the basename of file_path, the current date, and an incrementing counter."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    # Get today's date in YYYYMMDD format.
    today = datetime.datetime.now().strftime("%Y%m%d")
    # Extract the base name without extension.
    file_base = os.path.basename(file_path)
    if file_base.endswith(".yaml"):
        file_base = file_base[:-5]
    # Determine the next counter value for this base and date.
    pattern = os.path.join(log_dir, f"{file_base}_{today}_*.log")
    existing_logs = glob.glob(pattern)
    counter = 1
    for log in existing_logs:
        # Expect log filenames like "output_2d_chunks_20250315_001.log"
        try:
            # Get the last component after underscores and strip the .log part.
            num = int(os.path.splitext(log)[0].split("_")[-1])
            counter = max(counter, num + 1)
        except ValueError:
            continue
    # Format the counter as a three-digit number.
    counter_fmt = f"{counter:03d}"
    return os.path.join(log_dir, f"{file_base}_{today}_{counter_fmt}.log")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    print(f"Linting file: {file_path}")
    
    # Respect the FEKERR_YAML_CHECK environment variable (defaults to "1").
    if os.getenv("FEKERR_YAML_CHECK", "1") != "1":
        print(f"YAML lint check skipped for {file_path}")
        sys.exit(0)
    
    log_file = get_log_filename(file_path)
    # Run yamllint on the file.
    result = subprocess.run(["yamllint", file_path],
                            capture_output=True, text=True)
    
    # Write the output to the log file.
    with open(log_file, "w") as lf:
        lf.write(result.stdout)
        lf.write(result.stderr)
    
    # Echo the linting output.
    print(result.stdout)
    print(f"Lint output saved to {log_file}")
    
    # Exit with the same return code as yamllint.
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

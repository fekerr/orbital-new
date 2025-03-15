Below is an example of how you might reimplement your YAML checking wrapper in Python (to eventually replace the Bash script). This script, named `check_yaml.py`, replicates the functionality of the original `check_yaml.sh` but in Python. You can then update your Ninja rules to call this Python script instead.

The script does the following:

1. Expects a YAML filename as an argument.
2. Checks whether YAML linting is enabled via the environment variable `FEKERR_YAML_CHECK` (defaulting to 1).
3. Creates (if needed) a `logs` directory.
4. Constructs a log filename that includes the base name of the input file, today's date (in `YYYYMMDD` format), and an incrementing counter (formatted as three digits) so that multiple runs on the same day do not overwrite previous logs.
5. Executes `yamllint` via `subprocess.run()`, writes the output to the log file, echoes the output to stdout, and exits with the same return code as `yamllint`.

Save the following as **check_yaml.py**:

```python
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
```

### Integration with Ninja

Update your `build.ninja` file to use the new Python wrapper script by changing the YAML checking rule to call `check_yaml.py`:

```ninja
# Rule: Check a YAML file using the check_yaml.py wrapper script.
rule check_yaml
  command = python3 check_yaml.py $in
  description = "Checking YAML file $in with yamllint"
```

Make sure the rest of your Ninja file remains as before. This approach avoids the clunkiness of dollar-escaping in inline Bash commands by delegating the linting logic to a dedicated Python script.

### Additional Notes

- **Testing:**  
  Run the wrapper manually to verify it works:
  ```bash
  python3 check_yaml.py output_2d_chunks.yaml
  ```
- **Environment:**  
  Remember to run:
  ```bash
  source setenv.sh
  ```
  before invoking Ninja.
- **Future Enhancements:**  
  This Python script is easier to maintain and extend. For example, you can later add better error handling or more detailed logging using Python libraries.

Let me know if you need further modifications or additional features!

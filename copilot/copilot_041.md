Below is an updated version of the YAML-checking wrapper script (`check_yaml.sh`). This version does the following:

• Accepts a filename as its argument.  
• If YAML checking is enabled (via the environment variable `FEKERR_YAML_CHECK`, which defaults to 1), it runs `yamllint` on the file.  
• It writes the output of the linting process to a log file inside a `logs` directory.  
• The log file is named using today’s date in `YYYYMMDD` format followed by an incrementing counter (formatted as a three-digit number), so that no previous log is overwritten.

Save the following as `check_yaml.sh` in your repository and make sure it is executable:

```bash
#!/bin/bash
# check_yaml.sh
# This script checks a YAML file using yamllint and outputs the lint results
# to a log file in the "logs" directory. The log file is named using a timestamp
# in the format "YYYYMMDD_###.log" where ### is an incrementing value.
#
# Usage: ./check_yaml.sh <filename>
#
# It relies on the environment variable FEKERR_YAML_CHECK:
#   - If FEKERR_YAML_CHECK is 1 (default), the lint check is executed.
#   - If FEKERR_YAML_CHECK is 0, lint checking is skipped.

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>" >&2
    exit 1
fi

FILE="$1"
echo "Linting file: $FILE"

# Check if yaml linting is enabled (defaults to enabled if not set)
if [ "${FEKERR_YAML_CHECK:-1}" -ne 1 ]; then
    echo "YAML lint check skipped for $FILE"
    exit 0
fi

# Create logs directory if it doesn't exist.
LOGDIR="logs"
mkdir -p "$LOGDIR"

# Get today's date in YYYYMMDD format.
TODAY=$(date +%Y%m%d)

# Enable nullglob so that the glob returns an empty list if no files match.
shopt -s nullglob

# Determine the next counter value for today.
COUNTER=1
for LOGFILE in "$LOGDIR"/${TODAY}_*.log; do
    # Extract the counter from the filename.
    BASENAME=$(basename "$LOGFILE")         # e.g., 20250315_001.log
    NUM=${BASENAME#$TODAY_}                  # Remove the date prefix ==> "001.log"
    NUM=${NUM%%.log}                        # Remove the .log suffix  ==> "001"
    NUM_VAL=$(echo "$NUM" | sed 's/^0*//')    # Strip leading zeros.
    if [ -z "$NUM_VAL" ]; then
        NUM_VAL=0
    fi
    if [ "$NUM_VAL" -ge "$COUNTER" ]; then
        COUNTER=$((NUM_VAL + 1))
    fi
done

# Format the counter as a three-digit number.
COUNTER_FMT=$(printf "%03d" "$COUNTER")

# Compose the log file name.
LOGFILE_NAME="${TODAY}_${COUNTER_FMT}.log"
LOGFILE_PATH="$LOGDIR/$LOGFILE_NAME"

# Run yamllint and output both to the console and to the log file.
yamllint "$FILE" | tee "$LOGFILE_PATH"

echo "Lint output saved to $LOGFILE_PATH"
```

### How It Works

1. **Argument Checking:**  
   The script verifies that exactly one argument (the YAML file to be checked) is provided.

2. **YAML Check Decision:**  
   If `FEKERR_YAML_CHECK` is not set to 1 (the default), the check is skipped.

3. **Directory and Log Filename Creation:**  
   - It ensures a `logs` directory exists.  
   - It obtains today’s date in `YYYYMMDD` format.  
   - It uses the shell option `nullglob` to make sure that if no log files exist matching the pattern, the for-loop iterates over an empty list.
   - It scans through existing log files for today's date to determine the highest counter and then increments the counter.
   - The counter is formatted as a three-digit number (e.g., `001`), and the log file is named accordingly, for instance, `20250315_001.log`.

4. **YAML Linting and Logging:**  
   The output of `yamllint` is piped both to the console (with `tee`) and to the new log file.

---

### Integration with Ninja

With this script in place, your `build.ninja` file’s rule for YAML checking can now simply call this wrapper:

```ninja
# Rule: Check a YAML file using the check_yaml.sh wrapper script.
rule check_yaml
  command = ./check_yaml.sh $in
  description = "Checking YAML file $in with yamllint"
```

This approach eliminates the need for fiddly `$` escape sequences directly in `build.ninja` and makes your linting procedure clearer and easier to maintain.

Let me know if you need further adjustments or additional features!

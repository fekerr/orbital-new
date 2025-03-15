Below is an updated version of your `check_yaml.sh` wrapper that incorporates the checked filename into the log filename. Now, the log file name will include the basename of the YAML file (with the `.yaml` extension removed), followed by an underscore, the current date in `YYYYMMDD` format, and an incrementing three-digit counter. For example, if you are checking `output_2d_chunks.yaml`, the log might be named something like `output_2d_chunks_20250315_001.log`.

```bash
#!/bin/bash
# check_yaml.sh
# This script checks a YAML file using yamllint and outputs the lint results
# to a log file in the "logs" directory.
# The log file is named using the pattern: <basename>_YYYYMMDD_###.log,
# where <basename> is the base name of the file (without .yaml),
# YYYYMMDD is today's date, and ### is an incrementing counter.
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

# Check if YAML linting is enabled (defaults to enabled if not set)
if [ "${FEKERR_YAML_CHECK:-1}" -ne 1 ]; then
    echo "YAML lint check skipped for $FILE"
    exit 0
fi

# Create logs directory if it doesn't exist.
LOGDIR="logs"
mkdir -p "$LOGDIR"

# Get today's date in YYYYMMDD format.
TODAY=$(date +%Y%m%d)

# Extract the base name of the file (without the .yaml extension).
FILEBASE=$(basename "$FILE" .yaml)

# Enable nullglob so that the glob returns an empty list if no files match.
shopt -s nullglob

# Determine the next counter value for today for this FILEBASE.
COUNTER=1
for LOGFILE in "$LOGDIR"/${FILEBASE}_${TODAY}_*.log; do
    # Extract the counter from the filename.
    BASENAME=$(basename "$LOGFILE")         # e.g., output_2d_chunks_20250315_001.log
    # Remove prefix (FILEBASE and underscore + date and underscore) to get the counter.
    NUM=${BASENAME#${FILEBASE}_${TODAY}_}      # e.g., 001.log
    NUM=${NUM%%.log}                          # e.g., 001
    NUM_VAL=$(echo "$NUM" | sed 's/^0*//')      # Strip leading zeros.
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
LOGFILE_NAME="${FILEBASE}_${TODAY}_${COUNTER_FMT}.log"
LOGFILE_PATH="$LOGDIR/$LOGFILE_NAME"

# Run yamllint and output both to the console (via tee) and to the log file.
yamllint "$FILE" | tee "$LOGFILE_PATH"

echo "Lint output saved to $LOGFILE_PATH"
```

### Explanation

- **File Name Extraction:**  
  We use `basename "$FILE" .yaml` to strip the `.yaml` extension from the filename. This gives a base name (e.g., "output_2d_chunks") that is then incorporated into the final log filename.

- **Counter Calculation:**  
  The script searches for any existing logs matching the pattern `<FILEBASE>_<TODAY>_*.log` to find the highest counter and increments it by one.

- **Output Log File Naming:**  
  The final log file is built with the pattern `<FILEBASE>_<TODAY>_<COUNTER_FMT>.log`.

- **Logging:**  
  The output of `yamllint` is piped to both `tee` (thereby showing output in the terminal) and written into the log file.

### Integration with Ninja

Your `build.ninja` rule for YAML checking now calls this wrapper script. The relevant rule in your `build.ninja` remains:

```ninja
# Rule: Check a YAML file using the check_yaml.sh wrapper script.
rule check_yaml
  command = ./check_yaml.sh $in
  description = "Checking YAML file $in with yamllint"
```

This approach eliminates the need to manually escape dollar signs for the environment variables and simplifies maintenance. It also ensures that each checked file produces a uniquely named log that includes the file's name.

Let me know if you have further questions or need additional modifications!

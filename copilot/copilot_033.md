Below is an updated version addressing both points:

1. **For the Clean Target:**  
   Although your clean.sh already has an `rm -f output_2d_chunks.yaml output_3d_chunks.yaml` command, sometimes file‐location issues or typos can cause one file not to get removed. We can improve the script by:
   - Printing debug messages so you can see if the file exists.
   - Using an absolute (or working-directory–relative) path if needed.

2. **For the Environment Script (setenv.sh):**  
   Since setenv.sh is meant to be sourced (to modify your current shell’s environment), we should not mark it as executable—and we can add a check at the top so that if someone runs it directly, it complains and exits. This way, you “force” users to source it.

Below are the updated scripts:

---

### Updated clean.sh

```bash
#!/bin/bash
# clean.sh
# This script removes built files from the local machine while preserving the source code.
# It is intended to remove generated YAML file outputs.
# If a file is not present or not found, it will print a message.

set -e

echo "Cleaning generated build files..."

# Check and remove output_2d_chunks.yaml if it exists.
if [ -f "output_2d_chunks.yaml" ]; then
    echo "Removing output_2d_chunks.yaml..."
    rm -f output_2d_chunks.yaml
else
    echo "output_2d_chunks.yaml not found."
fi

# Check and remove output_3d_chunks.yaml if it exists.
if [ -f "output_3d_chunks.yaml" ]; then
    echo "Removing output_3d_chunks.yaml..."
    rm -f output_3d_chunks.yaml
else
    echo "output_3d_chunks.yaml not found."
fi

echo "Clean complete."
```

*This version prints messages for each file it tries to remove, making it easier to diagnose if one of the files isn’t in the expected location.*

---

### Updated setenv.sh

```bash
#!/bin/bash
# setenv.sh
#
# This script sets environment variables for the project.
# It is intended to be sourced (e.g., "source setenv.sh") to update your current shell's environment.
#
# Do not run this script directly; if executed, it will complain and exit.

# Check if the script is being sourced (BASH_SOURCE[0] vs. $0).
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "ERROR: setenv.sh is intended to be sourced. Please run: source setenv.sh" >&2
    exit 1
fi

# Export environment variables with defaults.
#
# FEKERR_YAML_CHECK:
#   Controls YAML linting (1 to enable [default], 0 to disable).
export FEKERR_YAML_CHECK=${FEKERR_YAML_CHECK:-1}

# GITUP_COUNT_FILE:
#   Specifies the file where the gitup script stores the commit count.
export GITUP_COUNT_FILE=${GITUP_COUNT_FILE:-commit_count.txt}

# You can add more environment variables here as needed.
echo "Environment variables set:"
echo "  FEKERR_YAML_CHECK = ${FEKERR_YAML_CHECK}"
echo "  GITUP_COUNT_FILE  = ${GITUP_COUNT_FILE}"
```

*By checking `if [[ "${BASH_SOURCE[0]}" == "${0}" ]]`, we ensure that if someone executes `./setenv.sh` instead of sourcing it, the script prints an error message and exits.*

---

### Integration with Ninja

Your updated `build.ninja` already calls other scripts—for example, for `install_tools`, `gitup`, and `clean`. Just make sure that before you run any Ninja targets, you run:
```bash
source setenv.sh
```
so that all the environment variables are correctly set.

---

### Summary

- **clean.sh:** Now prints messages when removing files, so you can see if one file (like the 3D output) is missing or in a different location.
- **setenv.sh:** Includes a check to ensure it’s sourced, not executed, so that it properly sets environment variables in your current shell.
- **Usage:**  
  Always run `source setenv.sh` before invoking Ninja, then run:
  ```bash
  ninja clean
  ```
  to clean built files, etc.

Let me know if you need further tweaks or additional features!

Below is an updated solution that avoids using a separate Makefile and instead integrates auxiliary targets directly via Ninja (and supporting wrapper scripts). Note that because environment variables (like those set by setenv.sh) only affect your current shell, you must run:

```bash
source setenv.sh
```

before invoking Ninja or any of the wrapper scripts. The updated solution consists of:

1. **gitup.sh** and **clean.sh** wrapper scripts that perform version-control tasks.
2. An updated **build.ninja** that adds generic targets for “gitup” and “clean” using those scripts.
3. A reminder that setenv.sh must be sourced manually.

---

### 1. gitup.sh

This script stages all changes, reads an incrementing commit number from a file (or uses an environment variable), commits with a message like `"gitup 001"`, and updates the count. Save this as `gitup.sh` and make it executable.

```bash
#!/bin/bash
# gitup.sh
# This script automates Git commits with an incrementing commit number.
# It stages all changes, commits with a message "gitup <number>",
# and updates the counter stored in a file specified by GITUP_COUNT_FILE.
#
# IMPORTANT: Be sure to source setenv.sh before running this script so that
#            the necessary environment variables are available.

set -e

# Use the environment variable GITUP_COUNT_FILE if set; otherwise default to commit_count.txt
GITUP_COUNT_FILE=${GITUP_COUNT_FILE:-commit_count.txt}

# Initialize the commit count file if it doesn't exist.
if [ ! -f "$GITUP_COUNT_FILE" ]; then
    echo "1" > "$GITUP_COUNT_FILE"
fi

commit_num=$(cat "$GITUP_COUNT_FILE")
echo "Current gitup commit number: $commit_num"

git add .
git commit -m "gitup $commit_num" || echo "Nothing to commit"

new_commit_num=$((commit_num + 1))
echo $new_commit_num > "$GITUP_COUNT_FILE"
echo "Updated commit count to $new_commit_num"
```

Make it executable:
```bash
chmod +x gitup.sh
```

---

### 2. clean.sh

This script removes only generated build files (for example, the YAML outputs). Save this as `clean.sh` and make it executable.

```bash
#!/bin/bash
# clean.sh
# This script removes built files from the local machine.
# It preserves your source code (and Git history) as a fallback backup.

set -e

echo "Cleaning generated build files..."
rm -f output_2d_chunks.yaml output_3d_chunks.yaml
echo "Clean complete."
```

Make it executable:
```bash
chmod +x clean.sh
```

---

### 3. Updated build.ninja

Now include generic targets in your Ninja build file for running these tasks along with your existing targets. Save the file as `build.ninja`:

```ninja
# build.ninja
#
# This file defines build targets using Ninja for our project.
# It includes targets for:
#   - Installing required tools.
#   - Building YAML chunks from Python files.
#   - Checking the generated YAML via yamllint.
#   - Running auxiliary scripts to commit (gitup) and clean built files.
#
# NOTE: Before running Ninja, run: source setenv.sh
#       This ensures that the environment variables needed by our scripts are set.

# ----------------------------------------------------------------------
# Rule to install required tools by running install_tools.sh.
rule install_tools
  command = ./install_tools.sh
  description = Installing required tools (Ninja, yamllint, and PyYAML)

# Phony target for installing tools (always runs).
build install_tools: phony install_tools.sh

# ----------------------------------------------------------------------
# Generic rule to build YAML chunks from a Python source file.
rule build_chunks
  command = python3 python_to_yaml.py $in $out
  description = Building YAML chunks from $in

# Build targets for generating YAML chunks.
build output_2d_chunks.yaml: build_chunks ../inner_solar_system_more_action_2d.py
build output_3d_chunks.yaml: build_chunks ../complete_solar_system_3d.py

# ----------------------------------------------------------------------
# Rule to check a YAML file using yamllint.
rule check_yaml
  command = bash -c 'if [ "${FEKERR_YAML_CHECK:-1}" -eq 1 ]; then yamllint "$in"; else echo "YAML lint check skipped for $in"; fi'
  description = "Checking YAML file $in with yamllint"

build check_2d_yaml: check_yaml output_2d_chunks.yaml
build check_3d_yaml: check_yaml output_3d_chunks.yaml
build yaml_check: phony check_2d_yaml check_3d_yaml

# ----------------------------------------------------------------------
# Rule for executing the gitup script.
rule gitup
  command = ./gitup.sh
  description = Executing gitup (auto-commit with incrementing number)

build gitup: phony gitup.sh

# Rule for executing the clean script.
rule clean
  command = ./clean.sh
  description = Cleaning built files

build clean: phony clean.sh

# ----------------------------------------------------------------------
# Phony "all" target that groups installation, building, YAML checking, gitup.
build all: phony install_tools output_2d_chunks.yaml output_3d_chunks.yaml yaml_check gitup

# Default target.
default all
```

---

### 4. setenv.sh

Ensure you have a file named `setenv.sh` that exports your environment variables. Because this file modifies your current shell’s environment, be sure to run it with `source` (or `.`):

```bash
#!/bin/bash
# setenv.sh
#
# Export environment variables for the project.
#
# FEKERR_YAML_CHECK:
#   Controls YAML linting. Set to 1 (default) to enable checks, 0 to disable.
export FEKERR_YAML_CHECK=1

# GITUP_COUNT_FILE:
#   Specifies the file where the gitup script stores the commit count.
export GITUP_COUNT_FILE=commit_count.txt

# Add more environment variables below as needed.
```

Make it executable (though typically you'll source it rather than execute):
```bash
chmod +x setenv.sh
```

---

### How to Use

1. **Initialize Environment:**
   Open your terminal and run:
   ```bash
   source setenv.sh
   ```
   This sets the required environment variables.

2. **Run Ninja Build:**
   Simply run:
   ```bash
   ninja
   ```
   The default target “all” will:
   - Install required tools (via install_tools.sh)
   - Build YAML chunks for both 2D and 3D scripts.
   - Check the YAML files with yamllint (if enabled).
   - Execute the gitup script, automatically committing your changes.
   
3. **Run Individual Targets:**
   You can execute individual targets if needed:
   - For just the “gitup” target:
     ```bash
     ninja gitup
     ```
   - To perform a clean:
     ```bash
     ninja clean
     ```

---

### Final Remarks

We’ve now integrated auxiliary tasks (gitup and clean) into Ninja so that everything can be managed through Ninja without needing a separate Makefile. Just remember to always source `setenv.sh` before running Ninja, so that the environment variables are available to the scripts.

Let me know if you need further adjustments or additional features!

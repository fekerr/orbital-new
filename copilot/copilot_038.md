Below is a complete version of your `build.ninja` file that incorporates all the targets to install tools, build YAML chunks, check the generated YAML files using yamllint (with proper escaping so that environment variables and Ninja variables are passed correctly), as well as auxiliary targets for gitup and cleaning built files. Remember that before you run Ninja, you should source your environment variables with:

```bash
source setenv.sh
```

Here’s the complete `build.ninja` file:

```ninja
# build.ninja
#
# This file defines build targets using Ninja for our project.
# It includes targets for:
#   - Installing required tools via install_tools.sh.
#   - Building YAML chunks from Python source files using python_to_yaml.py.
#   - Checking the generated YAML files using yamllint, controlled by the
#     environment variable FEKERR_YAML_CHECK.
#   - Executing auxiliary scripts (gitup.sh for auto-committing and clean.sh for cleaning build artifacts).
#
# NOTE: Before running Ninja, run:
#       source setenv.sh
# to ensure that the necessary environment variables are set.

# ----------------------------------------------------------------------
# Rule: Install required tools.
rule install_tools
  command = ./install_tools.sh
  description = Installing required tools (Ninja, yamllint, and PyYAML)

# Phony target for installing tools.
build install_tools: phony install_tools.sh

# ----------------------------------------------------------------------
# Rule: Build YAML chunks from a Python source file.
rule build_chunks
  command = python3 python_to_yaml.py $in $out
  description = Building YAML chunks from $in

# Targets to generate YAML chunks.
build output_2d_chunks.yaml: build_chunks ../inner_solar_system_more_action_2d.py
build output_3d_chunks.yaml: build_chunks ../complete_solar_system_3d.py

# ----------------------------------------------------------------------
# Rule: Check a YAML file using yamllint.
# Note: All literal dollars are escaped as $$ so that the shell receives the correct values.
rule check_yaml
  command = bash -c 'file="$${in}"; echo "Linting file: $$file"; if [ "$${FEKERR_YAML_CHECK:-1}" -eq 1 ]; then yamllint "$$file"; else echo "YAML lint check skipped for $$file"; fi'
  description = "Checking YAML file $$in with yamllint"

# Targets to check the generated YAML files.
build check_2d_yaml: check_yaml output_2d_chunks.yaml
build check_3d_yaml: check_yaml output_3d_chunks.yaml

# Group YAML check targets into a phony target.
build yaml_check: phony check_2d_yaml check_3d_yaml

# ----------------------------------------------------------------------
# Rule: Execute the gitup script (auto-commit with an incrementing number).
rule gitup
  command = ./gitup.sh
  description = Executing gitup (auto-commit with incrementing number)
build gitup: phony gitup.sh

# Rule: Execute the clean script to remove built files.
rule clean
  command = ./clean.sh
  description = Cleaning built files
build clean: phony clean.sh

# ----------------------------------------------------------------------
# Phony target 'all' groups the installation, build, YAML checking, and gitup tasks.
build all: phony install_tools output_2d_chunks.yaml output_3d_chunks.yaml yaml_check gitup

# Set the default target to 'all'.
default all
```

### Notes

- **Escaping `$` Signs:**  
  In the `check_yaml` rule, every `$` intended for the shell is written as `$$`. This ensures that when Ninja expands its variables (such as `$in`), the shell sees the correct values.
  
- **Environment Variable for YAML Linting:**  
  The rule uses `"$${FEKERR_YAML_CHECK:-1}"` so that if `FEKERR_YAML_CHECK` isn’t defined in your environment, it defaults to 1 (i.e. YAML linting is enabled).

- **Auxiliary Targets:**  
  The targets for `gitup` and `clean` are provided as phony targets so they can be run independently as needed:
  - To auto-commit your changes with an incrementing commit number, run:
    ```bash
    ninja gitup
    ```
  - To remove generated build files (YAML outputs), run:
    ```bash
    ninja clean
    ```

- **Default Target:**  
  Running `ninja` without arguments will execute the default `all` target, which installs tools, builds both YAML chunk files, verifies them with `yamllint` (if enabled), and runs the auto-commit script.

This integrated setup should streamline your build process and provide clear logging and error checking. Let me know if you need further modifications or additional features!

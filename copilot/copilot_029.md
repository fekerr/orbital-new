Below is an updated, complete `build.ninja` file that uses a generic rule to build YAML chunks from any Python file and includes a target for checking (linting) the generated YAML files. The YAML check is controlled by an environment variable (`FEKERR_YAML_CHECK`) that defaults to “true” (or 1) if not defined. You can later expand this variable to support multiple testing levels if needed.

In this approach, we use:
- A **generic build_chunks** rule for invoking your Python script that converts code to YAML.
- A **check_yaml** rule that calls a YAML linter (using `yamllint`) if `FEKERR_YAML_CHECK` is enabled.
- Grouped phony targets so that running `ninja` will install tools, generate chunks for both your 2D and 3D Python inputs, and then check the YAML structure.

Please note: While YAML is a popular choice for human‐readable configuration and documentation, you might also consider JSON or TOML depending on your goals. However, YAML remains a solid pick for flexibility, readability, and extensive tooling.

Below is the complete `build.ninja` file:

```ninja
# build.ninja
#
# This file defines build targets using Ninja for our project.
# It includes:
#
#   1. A generic target to install required tools by running install_tools.sh.
#   2. A generic build_chunks rule that converts a Python source file into a YAML file.
#   3. Rules to check the generated YAML files using yamllint.
#      The YAML linter is run conditionally, based on the environment variable FEKERR_YAML_CHECK.
#
# Environment Variable:
#   FEKERR_YAML_CHECK - If undefined or set to 1 (true), YAML linting is performed.
#                       If set to 0, the YAML check is skipped.
#
# Future enhancements could include more advanced AST-based parsing,
# an "imports section" (to consolidate import statements in the YAML),
# and even automatic diagram generation for code, data, and control flow.
#
# While YAML is standard for configuration and documentation, alternatives like JSON or TOML
# could be considered if strict schema validation is needed. For now, YAML remains a good choice.

# ----------------------------------------------------------------------
# Rule to install required tools by running install_tools.sh.
rule install_tools
  command = ./install_tools.sh
  description = Installing required tools (Ninja and PyYAML)

# Phony target for installing tools (always runs).
build install_tools: phony install_tools.sh

# ----------------------------------------------------------------------
# Generic rule to build YAML chunks from a Python source file.
rule build_chunks
  command = python3 python_to_yaml.py $in $out
  description = Building YAML chunks from $in

# Build targets for generating YAML chunks from given Python inputs.
build output_2d_chunks.yaml: build_chunks ../inner_solar_system_more_action_2d.py
build output_3d_chunks.yaml: build_chunks ../complete_solar_system_3d.py

# ----------------------------------------------------------------------
# Rule to check a YAML file using yamllint.
# This rule uses an inline bash command to check if the environment variable FEKERR_YAML_CHECK is 1 (or unset, defaulting to 1).
rule check_yaml
  command = bash -c 'if [ "${FEKERR_YAML_CHECK:-1}" -eq 1 ]; then yamllint "$in"; else echo "YAML lint check skipped for $in"; fi'
  description = "Checking YAML file $in with yamllint"

# Build targets to check the generated YAML files.
build check_2d_yaml: check_yaml output_2d_chunks.yaml
build check_3d_yaml: check_yaml output_3d_chunks.yaml

# Phony target grouping all YAML check targets.
build yaml_check: phony check_2d_yaml check_3d_yaml

# ----------------------------------------------------------------------
# Phony 'all' target groups installation, building, and YAML checking.
build all: phony install_tools output_2d_chunks.yaml output_3d_chunks.yaml yaml_check

# Set the default target so running "ninja" will execute 'all'.
default all
```

---

### Explanation & Next Steps

1. **Generic Build Rule (`build_chunks`):**  
   - This rule calls `python_to_yaml.py` with a specified input (`$in`) and output (`$out`), whether it is for 2D or 3D code.
   - You only need one rule here because the process is generic; you can add more specific rules later if needed.

2. **YAML Check Rule (`check_yaml`):**  
   - The command within this rule uses Bash to test if the environment variable `FEKERR_YAML_CHECK` is 1 (or not defined, which defaults to 1) and then runs `yamllint` on the given file.
   - If `FEKERR_YAML_CHECK` is set to 0, the YAML check is skipped.
   - This gives you control via environment variables and leaves room for more granular control in the future.

3. **Phony Targets & Default:**  
   - The `all` target groups the install, build, and check steps together.
   - Running `ninja` without any arguments will execute the `all` target.

4. **Tools & Future Enhancements:**
   - **YAML Linting:** We’re using `yamllint`; this is a standard tool for verifying YAML syntax.
   - **AST-based Extraction & Diagramming:** You mentioned using AST more deeply (for example, to extract import sections or generate structural diagrams). That’s a promising enhancement that can be introduced later.
   - **Alternatives to YAML:** YAML is popular and human readable, but if you later require a more schema-strict format, JSON or TOML are alternatives.
     
5. **Integration with Docker:**  
   - Your Dockerfile will call `install_tools.sh` to install all required tools, including Ninja and PyYAML, ensuring your containerized environment matches your host setup.

---

### How to Test

- **Run the Build Locally:**  
  Execute:
  ```bash
  ninja
  ```
  This will run the install step, generate YAML chunks from both input files, and run the YAML lint checks (provided `yamllint` is installed and `FEKERR_YAML_CHECK` is not set to 0).

- **Control YAML Checking:**  
  To skip YAML checking, run:
  ```bash
  FEKERR_YAML_CHECK=0 ninja
  ```
  Or set it in your environment before invoking Ninja.

---

Let me know if you need further refinements, additional targets, or more detailed guidance on using AST to extract more precise code structures for your YAML file!

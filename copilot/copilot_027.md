<build-environment> #004:

---

### Raw Prompt Input
```
$ ninja
Command 'ninja' not found, but can be installed with:
sudo apt install ninja-build

so add this to install_tools.sh and the docker file.
Actually, define this once and use it in the docker file.
```

---

### Restated Input Prompt
You want to ensure that Ninja is installed in your environment. Since Ninja isn’t found on your system, you’d like to modify your `install_tools.sh` script to automatically install Ninja (using apt-get) if it isn’t already available. Additionally, you want to integrate the Ninja installation into your Dockerfile by reusing the same `install_tools.sh` script rather than writing the installation commands twice. This ensures consistency between your host and Docker environments.

---

### Detailed Response

Below are the updated files with the required changes.

#### 1. Updated `install_tools.sh`

We modify the script to:
- Check if Ninja is installed.
- If not, install it using apt-get.
- Use a check for UID so that if running as root (as in a Docker build), it won’t use `sudo`.
- Then, upgrade pip and install PyYAML.

```bash
#!/bin/bash
# install_tools.sh
# This script installs required tools for the project.
# It ensures that Ninja is installed (using apt-get) and that Python dependencies (PyYAML) are installed.
# It checks whether it is running as root or a regular user to decide if 'sudo' is needed.

set -e  # Exit if any command fails

# Function to install Ninja if not present.
install_ninja() {
    if command -v ninja >/dev/null 2>&1; then
        echo "Ninja is already installed."
    else
        echo "Ninja not found, installing ninja-build..."
        if [ "$(id -u)" -eq 0 ]; then
            apt-get update && apt-get install -y ninja-build
        else
            sudo apt-get update && sudo apt-get install -y ninja-build
        fi
    fi
}

# Install Ninja using the function.
install_ninja

# Upgrade pip and install PyYAML.
pip3 install --upgrade pip
pip3 install PyYAML
```

*Make sure to mark the script as executable:*

```bash
chmod +x install_tools.sh
```

---

#### 2. Updated Dockerfile

We modify the Dockerfile to remove redundant installation of Ninja using apt-get and instead run our `install_tools.sh` script to install Ninja and PyYAML. This way, the installation logic is defined only once (in the script).

```dockerfile
# Dockerfile
FROM ubuntu:20.04

# Suppress interactive prompts for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install base packages essential for our environment.
# We no longer include ninja-build here since install_tools.sh handles it.
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the container working directory
WORKDIR /app

# Copy the entire repository into the container.
COPY . /app

# Ensure the install_tools.sh script is executable and run it.
RUN chmod +x install_tools.sh && \
    ./install_tools.sh

# Default command: open bash shell.
CMD ["bash"]
```

*Notes:*
- We removed explicit installation of `ninja-build` from the Dockerfile.
- The `install_tools.sh` script is invoked during the Docker build process to ensure consistent installation of both Ninja and PyYAML.

---

#### 3. Updated `build.ninja` (for context)

Your previously provided `build.ninja` file remains largely the same. It does not need alterations regarding Ninja, as we now ensure Ninja is installed via the script.

```ninja
# build.ninja
#
# This file defines build targets using Ninja.

# Rule to install required tools by running install_tools.sh.
rule install_tools
  command = ./install_tools.sh
  description = Installing required tools (Ninja and PyYAML)

# Phony target for installing tools (always runs).
build install_tools: phony install_tools.sh

# Rule for building YAML chunks using the python_to_yaml.py script.
rule build_chunks
  command = python3 python_to_yaml.py $in $out
  description = Building YAML chunks from $in

# Example target: Build YAML chunks from a specified input Python file.
build output_chunks.yaml: build_chunks ../inner_solar_system_more_action_2d.py

# Phony target 'all' to group targets.
build all: phony install_tools output_chunks.yaml

# Set default target.
default all
```

---

### Summary

- **`install_tools.sh`:**  
  Now automatically checks for and installs Ninja if it's missing and installs PyYAML. It distinguishes between root and non-root environments using `id -u`.

- **Dockerfile:**  
  Leverages `install_tools.sh` to install all required tools, thereby centralizing installation logic.

- **Usage:**  
  - On your host, running `./install_tools.sh` will ensure both Ninja and PyYAML are installed.
  - Building the Docker image will run the same script inside the container, ensuring a consistent environment.

This approach keeps your installation logic DRY (Don't Repeat Yourself) and consistent across your development and container environments. 

Let me know if you need further adjustments or additional features!

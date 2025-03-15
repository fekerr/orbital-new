Below is the updated version of your `install_tools.sh` that now also installs the YAML linting tool (yamllint) in addition to Ninja and PyYAML. This script checks for Ninja and yamllint, installing them if they're not present, and then upgrades pip and installs PyYAML via pip.

```bash
#!/bin/bash
# install_tools.sh
# This script installs required tools for the project:
#  - Ninja (using apt-get)
#  - yamllint (using pip3)
#  - Upgrades pip and installs PyYAML (using pip3)
#
# The script checks if it is running as root or a regular user to determine
# whether to use 'sudo' for apt-get commands.

set -e  # Exit immediately if any command exits with a non-zero status

# Function to install Ninja if it is not installed.
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

# Function to install yamllint if it is not installed.
install_yamllint() {
    if command -v yamllint >/dev/null 2>&1; then
        echo "yamllint is already installed."
    else
        echo "yamllint not found, installing yamllint via pip3..."
        pip3 install yamllint
    fi
}

# Install Ninja and yamllint using the functions above.
install_ninja
install_yamllint

# Upgrade pip and install PyYAML.
pip3 install --upgrade pip
pip3 install PyYAML

echo "All required tools have been installed."
```

### How This Works
- **install_ninja:**  
  Checks if the `ninja` command is available. If not, updates the package list and installs `ninja-build` using apt-get (using sudo if necessary).

- **install_yamllint:**  
  Checks for the presence of `yamllint`. If it’s not found, installs it via `pip3`. You can later switch to using a system package if desired.

- **Pip Operations:**  
  It upgrades pip and installs PyYAML, ensuring the necessary Python dependencies are available.

This script is now ready to be used both in your development environment and in your Dockerfile (by running it during the Docker build process) to ensure all tools are installed consistently.

Let me know if you need further modifications or additional features!

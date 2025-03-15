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

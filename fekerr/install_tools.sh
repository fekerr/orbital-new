#!/bin/bash
# install_tools.sh
# This script installs the required tools for the project:
#  - Ninja (using apt-get)
#  - yamllint (using pip3)
#  - PyYAML (using pip3)
#
# It first checks if the tools are already installed, and if not,
# installs them based on whether the script is running as root or as a normal user.
#
# Exit immediately if any command exits with a non-zero status.
set -e

# Function to install Ninja if it's not already installed.
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

# Function to install yamllint if it's not already installed.
install_yamllint() {
    if command -v yamllint >/dev/null 2>&1; then
        echo "yamllint is already installed."
    else
        echo "yamllint not found, installing yamllint via pip3..."
        pip3 install yamllint
    fi
}

# Run the installation functions.
install_ninja
install_yamllint

# Upgrade pip and install PyYAML.
pip3 install --upgrade pip
pip3 install PyYAML

echo "All required tools have been installed."

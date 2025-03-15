#!/bin/bash
# install_tools.sh
# This script installs the required Python packages for the project.
# Here, we upgrade pip and install PyYAML.

set -e  # Stop execution if any command fails

pip3 install --upgrade pip
pip3 install PyYAML

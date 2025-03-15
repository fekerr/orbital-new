#!/bin/bash
# check_yaml.sh
# This script checks a YAML file using yamllint.
# It uses the environment variable FEKERR_YAML_CHECK (default: 1) to control whether the check runs.
# Usage: ./check_yaml.sh <filename>

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>" >&2
    exit 1
fi

FILE="$1"
echo "Linting file: $FILE"
if [ "${FEKERR_YAML_CHECK:-1}" -eq 1 ]; then
    yamllint "$FILE"
else
    echo "YAML lint check skipped for $FILE"
fi

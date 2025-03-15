# setenv.sh
#
# This file sets environment variables for the project.
# It is intended to be sourced (e.g., "source setenv.sh") to update your current shell's environment.
# Do not mark this file as executable.
#
# Variables:
#
#   FEKERR_YAML_CHECK:
#       Controls YAML linting. Defaults to 1 (enabled). Set to 0 to disable.
#
#   GITUP_COUNT_FILE:
#       Specifies the file where the gitup script stores the commit count.
#
# If run directly (e.g., via "bash setenv.sh"), warn the user that it should be sourced.

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    echo "WARNING: This script is intended to be sourced, not executed." >&2
fi

export FEKERR_YAML_CHECK=${FEKERR_YAML_CHECK:-1}
export GITUP_COUNT_FILE=${GITUP_COUNT_FILE:-commit_count.txt}

echo "Environment variables set:"
echo "  FEKERR_YAML_CHECK = ${FEKERR_YAML_CHECK}"
echo "  GITUP_COUNT_FILE  = ${GITUP_COUNT_FILE}"

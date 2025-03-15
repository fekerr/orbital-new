#!/bin/bash
# setenv.sh
#
# This file defines environment variables used by the project.
# Source this file in your shell (e.g., "source setenv.sh") to set up your environment.
#
# Variables:
#
#   FEKERR_YAML_CHECK:
#       Controls YAML linting.
#       Set to 1 (default) to enable YAML lint checks.
#       Set to 0 to disable YAML linting during builds.
export FEKERR_YAML_CHECK=1

# GITUP_COUNT_FILE:
#       Specifies the file where the gitup target stores the commit count.
export GITUP_COUNT_FILE=commit_count.txt

# You can add more environment variables here as needed.

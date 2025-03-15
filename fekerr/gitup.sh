#!/bin/bash
# gitup.sh
# This script automates Git commits with an incrementing commit number.
# It stages all changes, commits with a message "gitup <number>",
# and updates the counter stored in a file specified by GITUP_COUNT_FILE.
#
# IMPORTANT: Be sure to source setenv.sh before running this script so that
#            the necessary environment variables are available.

set -e

# Use the environment variable GITUP_COUNT_FILE if set; otherwise default to commit_count.txt
GITUP_COUNT_FILE=${GITUP_COUNT_FILE:-commit_count.txt}

# Initialize the commit count file if it doesn't exist.
if [ ! -f "$GITUP_COUNT_FILE" ]; then
    echo "1" > "$GITUP_COUNT_FILE"
fi

commit_num=$(cat "$GITUP_COUNT_FILE")
echo "Current gitup commit number: $commit_num"

git add .
git commit -m "gitup $commit_num" || echo "Nothing to commit"

new_commit_num=$((commit_num + 1))
echo $new_commit_num > "$GITUP_COUNT_FILE"
echo "Updated commit count to $new_commit_num"

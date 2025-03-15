#!/bin/bash
# clean.sh
# This script removes built files from the local machine.
# It preserves your source code (and Git history) as a fallback backup.

set -e

echo "Cleaning generated build files..."
rm -f output_2d_chunks.yaml output_3d_chunks.yaml
echo "Clean complete."

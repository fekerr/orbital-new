# regex_utils.py
"""
regex_utils.py

This module provides utility functions encapsulating all regex-based logic
for our Python-to-YAML chunking tool. Separating regular expression code into
this module enhances maintainability and facilitates unit testing.

Functions:
    - is_chunk_marker(line: str, marker_pattern: str) -> bool
        Checks if a given line matches the specified chunk marker pattern.
    - is_blank_line(line: str) -> bool
        Determines if a line consists only of whitespace (i.e. a blank line).
"""

import re

def is_chunk_marker(line: str, marker_pattern: str) -> bool:
    """
    Checks whether the given line contains the chunk marker defined by the regex pattern.

    Parameters:
        line (str): A line from the source Python script.
        marker_pattern (str): A regex pattern to identify a chunk marker.
            (e.g., r'# --- CHUNK ---')

    Returns:
        bool: True if the line matches the marker, otherwise False.
    """
    pattern = re.compile(marker_pattern)
    return bool(pattern.search(line))

def is_blank_line(line: str) -> bool:
    """
    Returns True if the line is blank (contains only whitespace), False otherwise.

    Parameters:
        line (str): A string representing a line from a file.

    Returns:
        bool: True if the line is empty or only whitespace, False otherwise.
    """
    return bool(re.match(r'^\s*$', line))

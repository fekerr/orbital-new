#!/usr/bin/env python3
"""
regex_utils.py

This module includes utility functions for handling regular expressions in our project.
We use these functions to detect chunk markers in Python scripts. By isolating regex logic
in this module, we enhance maintainability, readability, and enable targeted unit testing.

Functions:
    - is_chunk_marker(line: str, marker_pattern: str) -> bool
        Checks if a given line matches the specified marker pattern.
"""

import re

def is_chunk_marker(line: str, marker_pattern: str) -> bool:
    """
    Determines whether the provided line qualifies as a chunk marker based on a regex pattern.
    
    Parameters:
        line (str): A string representing a single line from a Python script.
        marker_pattern (str): A regex pattern used to identify the chunk marker.
            For example, r'# --- CHUNK ---'
    
    Returns:
        bool: True if the line matches the marker pattern; otherwise, False.
    
    This function compiles the given pattern and checks if there is a match anywhere
    in the line. This abstraction is designed to keep the main chunking code clean and
    focused, while all regex complexities reside in this module.
    """
    # Compile the regex pattern.
    pattern = re.compile(marker_pattern)
    
    # Search for the pattern in the given line.
    match = pattern.search(line)
    
    # Return True if a match is found, else False.
    return bool(match)

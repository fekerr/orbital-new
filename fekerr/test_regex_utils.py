#!/usr/bin/env python3
"""
Unit tests for regex_utils.py
"""

import unittest
from regex_utils import is_chunk_marker

class TestRegexUtils(unittest.TestCase):
    def test_chunk_marker_found(self):
        # Test with a line that clearly contains the chunk marker pattern.
        marker_pattern = r'# --- CHUNK ---'
        line = "    # --- CHUNK ---"
        self.assertTrue(is_chunk_marker(line, marker_pattern))

    def test_chunk_marker_not_found(self):
        # Test with a line that does not contain the chunk marker.
        marker_pattern = r'# --- CHUNK ---'
        line = "print('Hello World')"
        self.assertFalse(is_chunk_marker(line, marker_pattern))

    def test_marker_with_additional_text(self):
        # Test a line where additional text follows the chunk marker.
        marker_pattern = r'# --- CHUNK ---'
        line = "# --- CHUNK --- Start of module imports"
        self.assertTrue(is_chunk_marker(line, marker_pattern))

    def test_case_sensitivity(self):
        # Test case-sensitive match. The marker is defined in uppercase.
        marker_pattern = r'# --- CHUNK ---'
        line = "# --- chunk ---"
        # Expect False because of case difference.
        self.assertFalse(is_chunk_marker(line, marker_pattern))

if __name__ == '__main__':
    unittest.main()

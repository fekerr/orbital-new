#!/usr/bin/env python3
"""
test_regex_utils.py

Unit tests for the regex utility functions in regex_utils.py.
These tests ensure that our regex-based helpers behave as expected.
"""

import unittest
from regex_utils import is_chunk_marker, is_blank_line

class TestRegexUtils(unittest.TestCase):
    def test_is_chunk_marker_found(self):
        marker_pattern = r'# --- CHUNK ---'
        line = "    # --- CHUNK ---"
        self.assertTrue(is_chunk_marker(line, marker_pattern))

    def test_is_chunk_marker_not_found(self):
        marker_pattern = r'# --- CHUNK ---'
        line = "print('Hello World')"
        self.assertFalse(is_chunk_marker(line, marker_pattern))

    def test_is_blank_line_true(self):
        self.assertTrue(is_blank_line("   "))
        self.assertTrue(is_blank_line("\n"))
        self.assertTrue(is_blank_line(""))

    def test_is_blank_line_false(self):
        self.assertFalse(is_blank_line("not blank"))
        self.assertFalse(is_blank_line("  data"))

if __name__ == '__main__':
    unittest.main()

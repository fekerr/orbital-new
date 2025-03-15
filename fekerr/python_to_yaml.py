#!/usr/bin/env python3
"""
python_to_yaml_chunks.py

This tool reads a large Python script and breaks it into chunks, outputting the result in a YAML file.
It uses a combination of AST-based parsing and heuristics (like long sequences of blank lines) 
to determine logical boundaries in the code automatically.

Each chunk includes:
    - A unique chunk ID.
    - A description.
    - An enable/disable flag.
    - The chunk's content.
    - Metadata placeholders (for performance, history, error bars).

The regex-related functions are delegated to the regex_utils.py module.
"""

import ast
import yaml
import sys
import os
from regex_utils import is_blank_line

def get_ast_boundaries(source):
    """
    Parses the source code using the AST and extracts boundaries for top-level nodes.

    Parameters:
        source (str): The full source code of the Python file.

    Returns:
        List[Tuple[int, int]]: A list of (start, end) line number tuples for each top-level node.

    Note:
        Python 3.8+ provides end_lineno for AST nodes. If not available, we approximate 
        the end by using the start of the next node.
    """
    boundaries = []
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print("Syntax error in source:", e)
        return boundaries

    # Ensure we have a list of top-level nodes.
    nodes = getattr(tree, "body", [])
    # Sort nodes by their starting line number
    nodes = sorted(nodes, key=lambda node: getattr(node, 'lineno', 0))

    for i, node in enumerate(nodes):
        start = getattr(node, 'lineno', 1)
        # If the node has an end_lineno attribute, use it; otherwise, use the start of the next node minus 1.
        if hasattr(node, 'end_lineno'):
            end = node.end_lineno
        else:
            if i + 1 < len(nodes):
                end = getattr(nodes[i + 1], 'lineno', start) - 1
            else:
                end = None  # Will handle later
        boundaries.append((start, end))
    return boundaries

def merge_with_heuristics(source_lines, ast_boundaries, min_blank_lines=2):
    """
    Uses AST boundaries combined with a heuristic: if there is a block of blank lines
    longer than min_blank_lines, it is also considered as a potential split point.

    Parameters:
        source_lines (List[str]): The full source code split into lines.
        ast_boundaries (List[Tuple[int, int]]): List of (start, end) tuples from the AST.
        min_blank_lines (int): Minimum number of consecutive blank lines to induce a new chunk.

    Returns:
        List[int]: A sorted list of line numbers where new chunks should start.
    """
    # Start with the boundaries from the AST: these indicate the start of top-level constructs.
    boundaries = set()
    for start, _ in ast_boundaries:
        boundaries.add(start)

    # Heuristic: check for long sequences of blank lines
    consecutive_blank = 0
    for i, line in enumerate(source_lines, start=1):  # Line numbers start at 1
        if is_blank_line(line):
            consecutive_blank += 1
        else:
            if consecutive_blank >= min_blank_lines:
                # Mark the line after the blank block as a boundary.
                boundaries.add(i)
            consecutive_blank = 0
    # Always include the first line as a boundary.
    boundaries.add(1)
    return sorted(boundaries)

def split_into_chunks(file_path):
    """
    Splits the Python file into chunks using a combination of AST boundaries and heuristic blank-line detection.

    Parameters:
        file_path (str): The path to the input Python script.

    Returns:
        List[Dict]: A list of chunk dictionaries.
    """
    with open(file_path, 'r') as f:
        source = f.read()
    source_lines = source.splitlines(keepends=True)

    # Get boundaries based on AST
    ast_boundaries = get_ast_boundaries(source)
    # Merge AST boundaries with blank-line heuristic
    all_boundaries = merge_with_heuristics(source_lines, ast_boundaries)

    chunks = []
    chunk_id = 1

    # Iterate over the boundaries to extract chunks.
    for i, start_line in enumerate(all_boundaries):
        # The chunk ends at one less than the next boundary, or the end of file.
        if i + 1 < len(all_boundaries):
            end_line = all_boundaries[i+1] - 1
        else:
            end_line = len(source_lines)
        content = ''.join(source_lines[start_line-1:end_line])
        chunks.append({
            'chunk_id': f'{chunk_id:03d}',
            'description': f'Chunk {chunk_id}',
            'enabled': True,
            'content': content,
            'metadata': {
                'performance': {},
                'history': f'Chunk generated from lines {start_line} to {end_line}.',
                'error_bars': None
            }
        })
        chunk_id += 1

    return chunks

    """
    TODO: some documentation may have been lost by copilot
    Writes the list of chunks into a YAML file.

    Parameters:
        chunks (List[Dict]): The list of chunk definitions.
        output_path (str): The output YAML file path.
    """

def write_yaml(chunks, output_path):
    """
    Writes the chunks to a YAML file.
    """
    with open(output_path, 'w') as f:
        # explicit_start=True forces what looks like a document start marker ('---') at the top.
        yaml.dump(chunks, f, sort_keys=False, explicit_start=True)

def main():
    if len(sys.argv) < 3:
        print("Usage: python python_to_yaml_chunks.py <input_py_file> <output_yaml_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Error: {input_file} does not exist.")
        sys.exit(1)

    chunks = split_into_chunks(input_file)
    write_yaml(chunks, output_file)
    print(f"YAML chunks written to {output_file}")

if __name__ == '__main__':
    main()

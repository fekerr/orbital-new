#!/usr/bin/env python3
"""
Tool: python_to_yaml_chunks.py

Purpose:
    - Read a large Python script.
    - Break it into manageable chunks using a defined marker.
    - Serialize these chunks into a YAML file with additional metadata.
    - Allow future processing such as selectively enabling/disabling chunks or optimization.

The tool leverages regex_utils.py for detecting chunk markers, thereby isolating all
regex-related code for maintainability and testing.
"""

import yaml
import sys
import os
from regex_utils import is_chunk_marker

def split_into_chunks(file_path, marker=r'# --- CHUNK ---'):
    """
    Splits a Python file into chunks using a specified chunk marker.
    
    Parameters:
        file_path (str): The path to the Python script to be split.
        marker (str): The regex pattern identifying a chunk delimiter.
    
    Returns:
        List[Dict]: A list of dictionaries, each representing a chunk with:
            - chunk_id: A unique identifier for the chunk.
            - description: A textual description.
            - enabled: A boolean flag to enable or disable the chunk.
            - content: The actual content of the chunk.
            - metadata: Additional metadata (e.g., performance metrics, history, error bars).
    """
    chunks = []
    current_chunk = []
    chunk_id = 1

    with open(file_path, 'r') as f:
        for line in f:
            # Use our utility function to check whether the current line is a chunk marker.
            if is_chunk_marker(line, marker):
                # When marker is encountered and if there's existing accumulated content, finalize a chunk.
                if current_chunk:
                    chunks.append({
                        'chunk_id': f'{chunk_id:03d}',
                        'description': f'Chunk {chunk_id}',
                        'enabled': True,
                        'content': ''.join(current_chunk),
                        'metadata': {
                            'performance': {},
                            'history': '',
                            'error_bars': None
                        }
                    })
                    chunk_id += 1
                    current_chunk = []  # Reset for the next chunk.
            else:
                current_chunk.append(line)
        # Add any remaining content as the final chunk.
        if current_chunk:
            chunks.append({
                'chunk_id': f'{chunk_id:03d}',
                'description': f'Chunk {chunk_id}',
                'enabled': True,
                'content': ''.join(current_chunk),
                'metadata': {
                    'performance': {},
                    'history': '',
                    'error_bars': None
                }
            })
    return chunks

def write_yaml(chunks, output_path):
    """
    Writes the list of chunk dictionaries to a YAML file.
    
    Parameters:
        chunks (list): The list of chunk dictionaries.
        output_path (str): The file path for the output YAML.
    """
    with open(output_path, 'w') as f:
        yaml.dump(chunks, f, sort_keys=False)

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

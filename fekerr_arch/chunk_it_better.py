import os
import sys

def chunk_file(input_file, max_chunk_size, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the file content
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Variables for chunking
    current_chunk = []
    current_size = 0
    chunk_number = 1

    # Process each line
    for line in lines:
        current_chunk.append(line)
        current_size += len(line.encode('utf-8'))

        if current_size >= max_chunk_size:  # Check if the current chunk exceeds size
            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_chunk_{chunk_number:03}.py")
            with open(output_file, 'w') as chunk:
                chunk.write(f"# Begin chunk {chunk_number:03}\n")
                chunk.writelines(current_chunk)
                chunk.write(f"# End chunk {chunk_number:03}\n")
            print(f"Created: {output_file}")
            
            # Reset for the next chunk
            current_chunk = []
            current_size = 0
            chunk_number += 1

    # Handle the last chunk
    if current_chunk:
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_chunk_{chunk_number:03}.py")
        with open(output_file, 'w') as chunk:
            chunk.write(f"# Begin chunk {chunk_number:03}\n")
            chunk.writelines(current_chunk)
            chunk.write(f"# End chunk {chunk_number:03}\n")
        print(f"Created: {output_file}")

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python chunk_it_better.py <filename> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    max_chunk_size = 9000  # Adjust max chunk size in bytes

    chunk_file(input_file, max_chunk_size, output_dir)

if __name__ == "__main__":
    main()


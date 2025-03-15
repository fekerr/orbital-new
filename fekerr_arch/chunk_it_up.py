import sys

def chunk_file(input_file, chunk_size, output_prefix):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    total_lines = len(lines)
    chunk_count = (total_lines // chunk_size) + (1 if total_lines % chunk_size != 0 else 0)

    for chunk_num in range(chunk_count):
        start = chunk_num * chunk_size
        end = start + chunk_size
        chunk_lines = lines[start:end]

        output_file = f"{output_prefix}_chunk_{chunk_num + 1:03}.py"
        with open(output_file, 'w') as chunk_file:
            chunk_file.write(f"# Begin chunk {chunk_num + 1:03}\n")
            chunk_file.writelines(chunk_lines)
            chunk_file.write(f"# End chunk {chunk_num + 1:03}\n")
        print(f"Created: {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python chunk_it.py <filename>")
        sys.exit(1)

    input_file = sys.argv[1]
    chunk_size = 500  # Number of lines per chunk
    output_prefix = input_file.split('.')[0]  # Use the input file name as prefix without extension

    chunk_file(input_file, chunk_size, output_prefix)

if __name__ == "__main__":
    main()


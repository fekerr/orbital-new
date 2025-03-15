import os

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

# Parameters
input_file = "complete_solar_system_3d.py"  # Replace with your file name
chunk_size = 500  # Adjust the number of lines per chunk
output_prefix = "copilot"  # Prefix for output files

chunk_file(input_file, chunk_size, output_prefix)


import sys
import os
import yaml

def extract_to_yaml(input_file, output_dir):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    data = {
        'configurations': [],
        'classes': []
    }

    current_class = None

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith('class '):
            current_class = {'name': stripped_line, 'content': []}
            data['classes'].append(current_class)
        elif current_class:
            current_class['content'].append(stripped_line)
            if stripped_line == '':
                current_class = None
        elif ' = {' in stripped_line:  # Rough way to identify configurations
            data['configurations'].append(stripped_line)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output YAML file name
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}.yaml")

    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    print(f"YAML file created: {output_file}")

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_to_yaml.py <filename> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    extract_to_yaml(input_file, output_dir)

if __name__ == "__main__":
    main()


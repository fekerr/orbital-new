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

        # Check for class definition
        if stripped_line.startswith('class '):
            current_class = {'name': stripped_line, 'content': []}
            data['classes'].append(current_class)
        elif current_class:
            if stripped_line.startswith('def '):
                current_class['content'].append({'method': stripped_line})
            else:
                current_class['content'].append(stripped_line)
            if stripped_line == '' and not current_class['content'][-1]:
                current_class = None

        # Check for configuration lines
        elif '=' in stripped_line and 'self.' in stripped_line:
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


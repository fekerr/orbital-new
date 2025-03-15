import sys
import yaml

def extract_to_yaml(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    data = {}
    data['content'] = ''.join(lines)

    with open(output_file, 'w') as f:
        yaml.dump(data, f)

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_to_yaml.py <filename> <output_filename>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    extract_to_yaml(input_file, output_file)

if __name__ == "__main__":
    main()


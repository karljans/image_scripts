#!/bin/bash

# Get the current working directory
current_directory="$(pwd)"

# Default directories
root_folder="$current_directory"
weight_file="$current_directory/weights/yolo.pt"

# Print the usage of this script
usage() {
    echo "Usage: $0 <root_folder>"
    echo "  <root_folder> - The root folder containing the rosbags. Default: $root_folder"
    echo "  <weight_file> - The weight file to use for the model. Default: $weight_file"
    exit 1
}

# Check if the number of arguments is larger than 1
if [ "$#" -gt 2 ]; then
    echo "Illegal number of arguments."
    usage
fi

# If the first argument is -h or --help, print the usage of this script
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
fi

# Get the root folder from the command line argument
root_folder_arg="$1"

if [ ! -z "$root_folder_arg" ]; then
    root_folder="$root_folder_arg"
fi

echo "Root folder: $root_folder"

# Check if the specified root folder exists
if [ ! -d "$root_folder" ]; then
    echo "Root folder does not exist."
    exit 1
fi

weight_file_arg="$2"

if [ ! -z "$weight_file_arg" ]; then
    weight_file="$weight_file_arg"
fi

# Check if the specified weight file exists
if [ ! -f "$weight_file" ]; then
    echo "Weight file does not exist."
    exit 1
fi

echo "Weight file: $weight_file"

# Path to the current script
script_path="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Use find command to list all sub-directories and their contents
# Then filter and run the specified command for each directory
find "$root_folder" -type d -links 2 -printf "%P\n" | while IFS= read -r directory; do
    echo "Creating label for directory: $current_directory/$directory"
    python3 "$script_path/create_labels.py" -i "$current_directory/$directory/" -w "$weight_file"
done

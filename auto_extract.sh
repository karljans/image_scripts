#!/bin/bash

# Get the current working directory
current_directory="$(pwd)"

# Default directories
root_folder="$current_directory/rosbags"
output_directory="$current_directory/pre_annotated_rosbag_imgs"

# Print the usage of this script
usage() {
    echo "Usage: $0 <root_folder> <output_directory>"
    echo "  <root_folder> - The root folder containing the rosbags. Default: $root_folder"
    echo "  <output_directory> - The output directory to store the extracted images. Default: $output_directory"
    exit 1
}

# Check if the number of arguments is larger than 2
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

# Check if the specified root folder exists
if [ ! -d "$root_folder" ]; then
    echo "Root folder does not exist."
    exit 1
fi

echo "Root folder: $root_folder"

# Read output directory from the command line argument
output_directory_arg="$2"

if [ ! -z "$output_directory_arg" ]; then
    output_directory="$output_directory_arg"
fi

# Check if the specified output directory exists
if [ ! -d "$output_directory" ]; then
    echo "Output directory does not exist, creating it..."
    mkdir -p "$output_directory"
fi

echo "Output directory: $output_directory"

# Path to the current script
script_path="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Use find command to list all sub-directories and their contents
# Then filter and run the specified command for each directory
find "$root_folder" -type d -links 2 -printf "%P\n" | while IFS= read -r directory; do
    full_path="$root_folder/$directory"
    python3 "$script_path/extract.py" -r "$full_path" -d "$output_directory/$directory"
done

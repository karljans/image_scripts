#!/bin/bash

# Function to remove zip files
remove_zip_files() {
  local dir="$1"
  
  # Use find to locate zip files and remove them
  find "$dir" -type f -name "*.zip" -exec rm -f {} \;
}

# Check if a directory is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 directory"
  exit 1
fi

# Check if the provided directory exists
if [ ! -d "$1" ]; then
  echo "Error: Directory '$1' not found."
  exit 1
fi

# Call the function to remove zip files recursively
remove_zip_files "$1"

echo "Zip files removed recursively from '$1'."

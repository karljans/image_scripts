#!/bin/bash

# Specify the root folder
root_folder="./AIRE_pre_annotated_rosbag_imgs/"

# Check if the specified root folder exists
if [ ! -d "$root_folder" ]; then
    echo "Root folder does not exist."
    exit 1
fi

# List of directory names to keep
directories_to_keep=(
    "_aftpi_oak_rgb_image_raw_compressed"
    "_frontpi_oak_rgb_image_raw_compressed"
    "_pspi_oak_rgb_image_raw_compressed"
    "_sbpi_oak_rgb_image_raw_compressed"
)

# Get the current working directory
current_directory="$(pwd)"

# Use find command to list all sub-directories and their contents
# Then filter and run the specified command for each directory
find "$root_folder" -type d -links 2 -printf "%P\n" | while IFS= read -r directory; do
    if [ -d "$root_folder/$directory" ]; then
        dir_name="$(basename "$root_folder/$directory")"
        if [[ ! " ${directories_to_keep[@]} " =~ " ${dir_name} " ]]; then
            echo "Removing directory: $directory"
            rm -rf "$root_folder/$directory"
        fi
    fi
done


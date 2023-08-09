#!/bin/bash

# Specify the root folder
root_folder="./rosbags/"

# Check if the specified root folder exists
if [ ! -d "$root_folder" ]; then
    echo "Root folder does not exist."
    exit 1
fi

# Get the current working directory
current_directory="$(pwd)"

# Use find command to list all sub-directories and their contents
# Then filter and run the specified command for each directory
find "$root_folder" -type d -links 2 -printf "%P\n" | while IFS= read -r directory; do
    full_path="$current_directory/rosbags/$directory"
    python3 /home/can/yolo_detection_train_test_tool/image_scripts/extract.py -r "$full_path" -d "$current_directory/AIRE_pre_annotated_rosbag_imgs/$directory"
done

import os
import re

# Function to find and return empty files
def remove_empty_files_images(directory):
    empty_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)
    return empty_files

# Check if a directory is provided as an argument
import sys

if len(sys.argv) != 2:
    print("Usage: python find_empty_files.py directory")
    sys.exit(1)

directory = sys.argv[1]

# Check if the provided directory exists
if not os.path.isdir(directory):
    print(f"Error: Directory '{directory}' not found.")
    sys.exit(1)

# Function to find and return files with a ".txt" extension
def existed_files(directory):
    e_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.strip().split(".")[-1] == "txt":
                e_files.append(file_path.strip().split(".txt")[0])
    return e_files

# Function to extract numeric suffix for sorting
def get_numeric_suffix(s):
    match = re.search(r'\d+$', s)
    return int(match.group()) if match else 0

# Call the function to find and print empty files recursively
ef = remove_empty_files_images(directory)
for f in ef:
    img_f = f.strip().split(".txt")[0]
    img_f += ".jpg"
    os.remove(f)
    os.remove(img_f)

# Find and sort files with a ".txt" extension
files = existed_files(directory)
sorted_files = sorted(files, key=get_numeric_suffix)

# Keep every 4th file and remove the rest
filtered_files = sorted_files[3::4]
cnt = 0

# Find the different elements between the two sets of files
different_elements = [item for item in sorted_files if item not in filtered_files] + [item for item in filtered_files if item not in sorted_files]

# Print some statistics
print("num files", len(sorted_files))
print("filt_files", len(filtered_files))
print("cnt", len(different_elements))    

# Remove ".txt" and ".jpg" files for the different elements
for f in different_elements:
    os.remove(f + ".txt")
    os.remove(f + ".jpg")
    
# Find and print the number of files left with ".txt" extension
files_left = existed_files(directory)
print("files_left", len(files_left))
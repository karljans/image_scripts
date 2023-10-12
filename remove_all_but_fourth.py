import os
import re
import natsort
import sys

# Only keep every 4th file
def remove_all_but_fourth(directory):   
    for root, _, files in os.walk(directory):
        filtered_files = []
        e_files = []
        different_elements = []
        sorted_files = []
        
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.strip().split(".")[-1] == "txt":
                e_files.append(file_path.strip().split(".txt")[0])
    
        print("len e files: ", len(e_files))
        sorted_files = natsort.natsorted(e_files)
    
        print("len sorted files: ", len(sorted_files))
        filtered_files = sorted_files[3::4]
    
        print("len filtered files: ", len(filtered_files))
        different_elements = [item for item in sorted_files if item not in filtered_files] + [item for item in filtered_files if item not in sorted_files]
    
        print("len different_elements: ", len(different_elements))
    
        for f in different_elements:
            os.remove(f + ".txt")
            os.remove(f + ".jpg")
        
if __name__ == "__main__":

    # Check if the user provided a directory
    if len(sys.argv) != 2:
        print("Usage: python find_empty_files.py directory")
        sys.exit(1)

    directory = sys.argv[1]

    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    remove_all_but_fourth(directory)

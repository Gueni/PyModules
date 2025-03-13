import os
from collections import defaultdict

def find_files_with_same_size(folder_path):
    # Dictionary to store file sizes as keys and list of file names with that size as values
    size_to_files = defaultdict(list)
    
    # Get all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            # Get file size in bytes
            file_size = os.path.getsize(file_path)
            # Append the file name to the list corresponding to its size
            size_to_files[file_size].append(file_name)
    
    # Filter and return only those sizes that have more than one file
    duplicate_size_files = {size: files for size, files in size_to_files.items() if len(files) > 1}
    
    return duplicate_size_files

#---------------------------------------------------------------------
if __name__ == "__main__":
    destination_folder = "D:/PC"
    duplicate_files = find_files_with_same_size(destination_folder)
    
    if duplicate_files:
        print("Files with the same size:")
        for size, files in duplicate_files.items():
            print(f"\nSize: {size} bytes")
            for file in files:
                # Strip the .mp4 extension when printing
                file_without_extension = os.path.splitext(file)[0]
                print(f" - {file_without_extension}")
    else:
        print("No files with the same size were found.")
#---------------------------------------------------------------------

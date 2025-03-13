import os
import shutil

def move_files_to_parent(parent_folder):
    # Walk through the directory structure
    for root, dirs, files in os.walk(parent_folder, topdown=False):
        # Move each file in the current directory (root) to the parent folder
        for file_name in files:
            file_path = os.path.join(root, file_name)
            new_path = os.path.join(parent_folder, file_name)
            
            if file_path != new_path:  # Prevent moving files that are already in the parent folder
                shutil.move(file_path, new_path)
                print(f"Moved: {file_path} to {new_path}")

        # Remove the directory if it is empty
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if the directory is empty
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")

# Example usage
folder_path = 'E:\PERSONAL\ME\VID'
move_files_to_parent(folder_path)

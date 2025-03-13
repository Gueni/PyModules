import os
from pathlib import Path

def sort_files_by_creation_date(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out only files (not directories)
    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

    # Sort files by their creation date
    files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))

    # Add a number to the beginning of their names
    for index, file in enumerate(files):
        new_name = f"{index:02d}.mp4"#_{file}"
        # new_name = new_name[10:]
        os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))

if __name__ == "__main__":
    folder_path  = "D:/8 PC/"
    sort_files_by_creation_date(folder_path)



import webbrowser
import time
import os,shutil
from pathlib import Path

link_dict  = [
]

def rename_files(folder_path,destination_folder):
    file_list = os.listdir(folder_path)  # Get the list of file names in the folder

    for file_name in file_list:
       if file_name.endswith(".mp4_") or file_name.endswith(".mp4"):
            old_file_path = os.path.join(folder_path, file_name)
            new_file_name = file_name[:-5] + str(".mp4")
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(old_file_path, new_file_path)  # Rename the file
            #move file to destination            
            shutil.move(new_file_path, destination_folder)

def sort_files_by_creation_date(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out only files (not directories)
    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

    # Sort files by their creation date
    files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))

    # Add a number to the beginning of their names
    for index, file in enumerate(files):
        new_name = f"{index:03d}.mp4"#_{file}"
        # new_name = new_name[10:]
        os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))

#---------------------------------------------------------------------
folder_path         = ""
destination_folder  = ""
i=1
for val in link_dict:
    print(len(link_dict)-(i-1),i)
    webbrowser.open(val)
    time.sleep(600)
    rename_files(folder_path,destination_folder)
    sort_files_by_creation_date(destination_folder)
    i+=1
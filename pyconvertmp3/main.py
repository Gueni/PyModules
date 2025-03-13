import os
import subprocess

# Define paths
webm_path = "D:/WORKSPACE/Python_code/pyconvertmp3/music"
mp3path = "D:/WORKSPACE/Python_code/pyconvertmp3/mp3"
bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Full path to Python executable
python_executable = r"C:/Users/Mohamed Gueni/AppData/Local/Programs/Python/Python313/python.exe"

# Full path to the script
webm2mp3_script = os.path.join(bundle_dir, 'webm2mp3.py')

# Construct the command as a list
command = [
    python_executable,
    webm2mp3_script,
    "--webm_path", webm_path,
    "--mp3_path", mp3path
]

# Execute the command
subprocess.run(command, check=True)

import os
import subprocess

# Define paths
webm_path = ""
mp3path = ""
bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Full path to Python executable
python_executable = r""

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

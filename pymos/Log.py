
#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                 ______  ____  _______  _____
#?                / __ \ \/ /  |/  / __ \/ ___/
#?               / /_/ /\  / /|_/ / / / /\__ \
#?              / ____/ / / /  / / /_/ /___/ /
#?             /_/     /_/_/  /_/\____//____/
#?
#? Name:        Log.py
#? Purpose:     Log simulation parameters and results into .log and .json formats
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import json
import os
from datetime import datetime

#? -------------------------------------------------------------------------------
class Logger:
    def __init__(self, log_dir=r"D:\WORKSPACE\Python_code\pymos\data"):
        self.log_dir        = log_dir
        self.log_path_txt   = os.path.join(log_dir, "vars.log")
        self.log_path_json  = r'D:\WORKSPACE\Python_code\pymos\vars.json'
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, quantities):
        self._write_txt_log(quantities)
        print(f"Logged to:\n- {self.log_path_txt}\n- {self.log_path_json}")

    def load_parameters(self):
        with open(self.log_path_json, "r") as f:
            data = json.load(f)
        return {k: v["VALUE"] for k, v in data.items()}

    def _write_txt_log(self, quantities):
        with open(self.log_path_txt, "w") as txt_file:
            txt_file.write("=" * 100 + "\n")
            txt_file.write(f"# Log generated on {datetime.now()}\n")
            txt_file.write("=" * 100 + "\n")
            txt_file.write(f"{'Quantity':<25}{'VALUE':<15}{'UNIT':<10}{'DESCRIPTION':<40}\n")
            txt_file.write("=" * 100 + "\n")
            items = list(quantities.items())
            for i, (key, entry) in enumerate(items):
                txt_file.write(f"{key:<25}{entry['VALUE']:<15g}{entry.get('UNIT', ''):<10}{entry.get('DESCRIPTION', ''):<60}\n")
                if i < len(items) - 1:
                    txt_file.write("-" * 100 + "\n")
            txt_file.write("=" * 100 + "\n")
#? -------------------------------------------------------------------------------
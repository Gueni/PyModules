# D:\WORKSPACE\Python_code\pymos\Log.py
# D:\WORKSPACE\Python_code\pymos\Log.py

import json
import os
from datetime import datetime


class Logger:
    def __init__(self, log_dir=r"D:\WORKSPACE\Python_code\pymos\data"):
        self.log_dir = log_dir
        self.log_path_txt = os.path.join(log_dir, "vars.log")
        self.log_path_json = os.path.join(log_dir, "vars.json")
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, quantities):
        self._write_txt_log(quantities)
        print(f"Logged to:\n- {self.log_path_txt}\n- {self.log_path_json}")

    def _write_txt_log(self, quantities):
        with open(self.log_path_txt, "w") as txt_file:
            txt_file.write("=" * 100 + "\n")
            txt_file.write(f"# Log generated on {datetime.now()}\n")
            txt_file.write("=" * 100 + "\n")
            txt_file.write(f"{'Quantity':<25}{'Value':<15}{'Unit':<10}{'Description':<40}\n")
            txt_file.write("=" * 100 + "\n")
            items = list(quantities.items())
            for i, (key, entry) in enumerate(items):
                txt_file.write(f"{key:<25}{entry['value']:<15g}{entry.get('unit', ''):<10}{entry.get('desc', ''):<60}\n")
                if i < len(items) - 1:
                    txt_file.write("-" * 100 + "\n")
            txt_file.write("=" * 100 + "\n")



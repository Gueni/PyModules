
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
import os
import json
from datetime import datetime
import textwrap
from rich.console import Console
from rich.table import Table
import textwrap
#? -------------------------------------------------------------------------------

class Logger:
    def __init__(self, log_dir=r"D:\WORKSPACE\PyModules\10_pymos\data"):
        self.log_dir        = log_dir
        self.log_path_txt   = os.path.join(log_dir, "vars.log")
        self.log_path_json  = r'D:\WORKSPACE\PyModules\10_pymos\src\vars.json'
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, quantities):
        self._write_txt_log(quantities)
        print(f"Logged to:\n- {self.log_path_txt}\n- {self.log_path_json}")

    def load_parameters(self):
        with open(self.log_path_json, "r") as f:
            data = json.load(f)
        return data  # Return full structure


    def _write_txt_log(self, quantities):
        console = Console(record=True, width=130) 
        table = Table(title="Parameter Log", show_lines=True, expand=True)
        table.add_column("Quantity", style="cyan", no_wrap=True)
        table.add_column("VALUE", style="green", justify="right")
        table.add_column("UNIT", style="magenta")
        table.add_column("DESCRIPTION", style="white")
        for key, entry in quantities.items():
            value = entry.get("VALUE", "")
            unit = entry.get("UNIT", "")
            description = entry.get("DESCRIPTION", "")
            wrapped_desc = "\n".join(textwrap.wrap(description, width=60))
            table.add_row(str(key), str(value), str(unit), wrapped_desc)
        console.print(table)
        with open(self.log_path_txt, "w", encoding="utf-8") as f:
            f.write("=" * 130 + "\n")
            f.write(f"# Log generated on {datetime.now()}\n")
            f.write("=" * 130 + "\n")
            f.write(console.export_text())
            f.write("=" * 130 + "\n")

#? -------------------------------------------------------------------------------
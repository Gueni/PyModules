
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
#? Name:        main.py
#? Purpose:     Main entry point for running simulations using the pymos models
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import numpy as np
import pandas as pd
import os
import Id_BSIM3v3
import Id_shichman_hodges
import Caps_BSIM3v3
import Caps_shichman_hodges
from Plot import MOSFETPlotter
from plot_compare import MOSFETModelComparer
import Log
import json
#? -------------------------------------------------------------------------------
# Simulation sweep settings
Vgs_values = np.linspace(0.0, 20.0, 9)           # 0V to 20V
Vds_values = np.linspace(0.0, 800.0, 9)          # 0V to 800V
T_values   = [300, 325, 350, 375, 400, 425, 450] # Kelvin

Plot = False
# Paths for data output
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
SH_PATH = os.path.join(DATA_DIR, "shichman_hodges.csv")
BSIM3_PATH = os.path.join(DATA_DIR, "BSIM3v3.csv")
json_path = r'D:\WORKSPACE\Python_code\pymos\vars.json'
with open(json_path, 'r') as file:
    data_dict = json.load(file)
#? -------------------------------------------------------------------------------
def main():
    # Instantiate models
    sh_model = Id_shichman_hodges.ShichmanHodgesModel()
    bsim3_model = Id_BSIM3v3.BSIM3v3Model()
    sh_caps = Caps_shichman_hodges.ShichmanHodgesCapacitances()
    bsim3_caps = Caps_BSIM3v3.BSIM3v3Capacitances()

    logger = Log.Logger()
    logger.log(data_dict)

    # --- Simulate Shichman-Hodges ---
    print("Simulating Shichman-Hodges model...")
    sh_records = []
    for T in T_values:
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                Id = sh_model.compute_Id(Vgs, Vds)
                Cgs, Cgd, Cds = sh_caps.compute(Vgs, Vds)
                sh_records.append({
                    'time': 0,
                    'T': T,
                    'VGS': Vgs,
                    'VDS': Vds,
                    'ID': Id,
                    'CGS': Cgs,
                    'CGD': Cgd,
                    'CDS': Cds
                })

    sh_df = pd.DataFrame(sh_records)
    sh_df['time'] = np.linspace(0, 1.0, len(sh_df))
    sh_df.to_csv(SH_PATH, index=False)
    print(f"Saved Shichman-Hodges simulation to {SH_PATH}")

    # --- Simulate BSIM3v3 ---
    print("Simulating BSIM3v3 model...")
    bsim3_records = []
    for T in T_values:
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                Id = bsim3_model.compute_Id(Vgs, Vds)
                Cgs, Cgd, Cds = bsim3_caps.compute(Vgs, Vds)
                bsim3_records.append({
                    'time': 0,
                    'T': T,
                    'VGS': Vgs,
                    'VDS': Vds,
                    'ID': Id,
                    'CGS': Cgs,
                    'CGD': Cgd,
                    'CDS': Cds
                })

    bsim3_df = pd.DataFrame(bsim3_records)
    bsim3_df['time'] = np.linspace(0, 1.0, len(bsim3_df))
    bsim3_df.to_csv(BSIM3_PATH, index=False)
    print(f"Saved BSIM3v3 simulation to {BSIM3_PATH}")

    # --- Compare the two models ---
    if Plot:
        print("Plotting comparison of Shichman-Hodges and BSIM3v3...")
        sh_plotter = MOSFETPlotter(SH_PATH)
        bsim3_plotter = MOSFETPlotter(BSIM3_PATH)
        sh_plotter.plot()
        bsim3_plotter.plot()
        print("Comparing Shichman-Hodges and BSIM3v3...")
        compare_plotter = MOSFETModelComparer(SH_PATH, BSIM3_PATH)
        compare_plotter.plot()
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#? -------------------------------------------------------------------------------
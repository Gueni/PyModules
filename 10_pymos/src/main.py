
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
import LV_13_BSIM3v3
import LV_1_Shichman_Hodges
from Plot import MOSFETModelComparer
import Log
#? -------------------------------------------------------------------------------
Vgs_values      = np.linspace(0.0, 20.0, 9)           # 0V to 20V
Vds_values      = np.linspace(0.0, 800.0, 9)          # 0V to 800V
T_values        = [300, 325, 350, 375, 400, 425, 450] # Kelvin
Plot            = False
SH_PATH         = r"D:\WORKSPACE\PyModules\10_pymos\data\shichman_hodges.csv"
BSIM3_PATH      = r"D:\WORKSPACE\PyModules\10_pymos\data\BSIM3v3.csv"
json_path       = r'D:\WORKSPACE\PyModules\10_pymos\src\vars.json'
data_dict       = Log.Logger().load_parameters()    
#? -------------------------------------------------------------------------------
def main():
    sh_model    = LV_1_Shichman_Hodges.ShichmanHodgesModel()
    bsim3_model = LV_13_BSIM3v3.BSIM3v3Model()
    logger      = Log.Logger()
    logger.log(data_dict)

    # --- Simulate Shichman-Hodges ---
    print("Simulating Shichman-Hodges model...")
    sh_records = []
    for T in T_values:
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                Id              = sh_model._ID_(Vgs, Vds)
                Cgs, Cgd, Cds   = sh_model._Caps_(Vgs, Vds)
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

    sh_df           = pd.DataFrame(sh_records)
    sh_df['time']   = np.linspace(0, 1.0, len(sh_df))
    sh_df.to_csv(SH_PATH, index=False)
    print(f"Saved Shichman-Hodges simulation to {SH_PATH}")

    # --- Simulate BSIM3v3 ---
    print("Simulating BSIM3v3 model...")
    bsim3_records = []
    for T in T_values:
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                Id              = bsim3_model._ID_(Vgs, Vds)
                Cgs, Cgd, Cds   = bsim3_model._Caps_(Vgs, Vds)
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

    bsim3_df         = pd.DataFrame(bsim3_records)
    bsim3_df['time'] = np.linspace(0, 1.0, len(bsim3_df))
    bsim3_df.to_csv(BSIM3_PATH, index=False)
    print(f"Saved BSIM3v3 simulation to {BSIM3_PATH}")

    # --- Compare the two models ---
    if Plot:
        compare_plotter = MOSFETModelComparer(SH_PATH, BSIM3_PATH)
        compare_plotter.plot()
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#? -------------------------------------------------------------------------------
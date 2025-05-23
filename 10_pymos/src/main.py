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
Vgs_values  = np.linspace(0.0, 20.0, 9)
Vds_values  = np.linspace(0.0, 800.0, 9)
T_values    = [300, 325, 350, 375, 400, 425, 450]
SH_PATH     = r"D:\WORKSPACE\PyModules\10_pymos\data\shichman_hodges.csv"
BSIM3_PATH  = r"D:\WORKSPACE\PyModules\10_pymos\data\BSIM3v3.csv"
PLOT        = False
logger      = Log.Logger()
data_dict   = logger.load_parameters()
sh_model    = LV_1_Shichman_Hodges.ShichmanHodgesModel()
bsim3_model = LV_13_BSIM3v3.BSIM3v3Model()
#? -------------------------------------------------------------------------------
def simulate_model(model, T_values, Vgs_values, Vds_values, path):
    records         = []
    combinations    = [(T, Vgs, Vds) for T in T_values for Vgs in Vgs_values for Vds in Vds_values]
    total_points    = len(combinations)

    for i, (T, Vgs, Vds) in enumerate(combinations):
        Id              = model._ID_(Vgs, Vds, T=T)
        Cgs, Cgd, Cds   = model._Caps_(Vgs, Vds)
        records.append({
            'time'  : i / total_points,
            'T'     : T,
            'VGS'   : Vgs,
            'VDS'   : Vds,
            'ID'    : Id,
            'CGS'   : Cgs,
            'CGD'   : Cgd,
            'CDS'   : Cds
        })

    df = pd.DataFrame(records)
    df.to_csv(path, index=False)

def main():
    logger.log(data_dict)
    simulate_model(sh_model     , T_values, Vgs_values, Vds_values, SH_PATH     )
    simulate_model(bsim3_model  , T_values, Vgs_values, Vds_values, BSIM3_PATH  )

    if PLOT:
        plotter = MOSFETModelComparer(SH_PATH, BSIM3_PATH)
        plotter.plot()

#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#? -------------------------------------------------------------------------------

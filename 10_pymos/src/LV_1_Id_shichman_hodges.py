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
#? Name:        Id_shichman_hodges.py
#? Purpose:     Compute drain current using the Shichman-Hodges model
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------

import Log
from Equations import Equations
import numpy as np

#? -------------------------------------------------------------------------------
class ShichmanHodgesModel:
    def __init__(self):
        logger          = Log.Logger()
        self.eq         = Equations()
        self.params     = logger.load_parameters()
        self.mu         = self.params["UO"]["VALUE"]               
        self.C_ox       = self.params["COX"]["VALUE"]              
        self.lambda_    = self.params["lambda_"]["VALUE"]           
        self.KP         = self.mu * self.C_ox  # or self.params["KP_N"]["VALUE"] for NMOS or self.params["KP_P"]["VALUE"] for PMOS
        self.scale      = 0.0
        LMLT            = self.params["LMLT"]["VALUE"]
        WMLT            = self.params["WMLT"]["VALUE"]
        L_scaled        = self.params["L"]["VALUE"]     * self.scale
        W_scaled        = self.params["W"]["VALUE"]     * self.scale
        XL_scaled       = self.params["XL"]["VALUE"]    * self.scale
        XW_scaled       = self.params["XW"]["VALUE"]    * self.scale
        LD_scaled       = self.params["LD"]["VALUE"]    * self.scale
        DEL_scaled      = self.params["DEL"]["VALUE"]   * self.scale
        WD_scaled       = self.params["WD"]["VALUE"]    * self.scale

        #todo : check the scaling and the units and the fromula for L and W
        self.L_eff      = 1 # L_scaled * LMLT + XL_scaled - 2*(LD_scaled + DEL_scaled) 
        self.W_eff      = 1 # 1 * ( W_scaled * WMLT + XW_scaled - 2 * WD_scaled) 


    def compute_Id(self, Vgs, Vds, Vsb=0.0):
        Vth             = self.eq.compute_Vth(Vsb)
        Vsat            = self.eq.clip(Vgs - Vth)
        W_over_L        = self.W_eff / self.L_eff

        if   Vsat      <= 0     :   region = "cutoff"       #! Vgs <= Vth
        elif Vsat      >= Vds   :   region = "linear"       #! vds <= vgs-Vth
        elif Vsat      <  Vds   :   region = "saturation"   #! Vds >= Vgs - Vth

        match region:
            case "cutoff"       :   Id = 0.0
            case "linear"       :   Id = self.KP * W_over_L * (1 + self.lambda_ * Vds) * (Vsat - (Vds/2)) * Vds
            case "saturation"   :   Id = 1/2 * self.KP * W_over_L * (1 + self.lambda_ * Vds) * np.square(Vsat)
        return self.eq.clip(Id)
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    model = ShichmanHodgesModel()
    Vgs , Vds , Vsb = 15 , 600 , 1.0
    Id              = model.compute_Id(Vgs=15, Vds=600, Vsb=1.0)
    print(f"ID_ShichmanHodges(Vgs={Vgs}, Vds={Vds}, Vsb={Vsb}) = {Id:.6e} A")
#? -------------------------------------------------------------------------------

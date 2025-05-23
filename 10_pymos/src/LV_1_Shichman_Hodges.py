
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
#? Name:        LV_1_Shichman_Hodges.py
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
        self.mu         = self.params["mu"]["VALUE"]               
        self.C_ox       = self.params["C_ox"]["VALUE"]              
        self.lambda_    = self.params["lambda_"]["VALUE"]           
        self.KP         = 2.0718e-5 #self.mu * self.C_ox
        self.L_eff      = 1 # L_scaled * LMLT + XL_scaled - 2*(LD_scaled + DEL_scaled) 
        self.W_eff      = 1 # 1 * ( W_scaled * WMLT + XW_scaled - 2 * WD_scaled) 
        self.C_g_total  = self.C_ox 

    def compute(self, Vgs, Vds, Vsb=0.0, T=350):
        Vth             = self.eq.compute_Vth(Vsb,T)
        Vsat            = Vgs - Vth
        W_over_L        = self.W_eff / self.L_eff

        if   Vsat      <= 0     :   region = "cutoff"       #! Vgs <= Vth
        elif Vsat      >= Vds   :   region = "linear"       #! vds <= vgs-Vth
        elif Vsat      <  Vds   :   region = "saturation"   #! Vds >= Vgs - Vth

        match region:
            case "cutoff"       :   
                        Id  = 0.0
                        Cgs = 0.0
                        Cgd = 0.0
                        Cds = 0.0
            case "linear"       :   
                        Id  = self.KP * W_over_L * (1 + self.lambda_ * Vds) * (Vsat - (Vds/2)) * Vds
                        Cgs = 0.0
                        Cgd = 0.0
                        Cds = 0.0
            case "saturation"   :   
                        Id  = 1/2 * self.KP * W_over_L * (1 + self.lambda_ * Vds) * np.square(Vsat)
                        Cgs = 0.0
                        Cgd = 0.0
                        Cds = 0.0
        return Id,Cgs, Cgd, Cds
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    model               = ShichmanHodgesModel()
    Vgs , Vds , Vsb ,T  = 15 , 600 , 0.0 , 300
    Id,Cgs, Cgd, Cds    = model.compute(Vgs=Vgs, Vds=Vds,Vsb=Vsb,T=T)
    print("-------------------------------------------------------")
    print(f"\n(Vgs={Vgs}, Vds={Vds}, Vsb={Vsb})")
    print(f"\nID  = {Id:.6e} A")
    print(f"Cgs = {Cgs:.3e} F\nCgd = {Cgd:.3e} F\nCds = {Cds:.3e} F")
    print("-------------------------------------------------------")
#? -------------------------------------------------------------------------------

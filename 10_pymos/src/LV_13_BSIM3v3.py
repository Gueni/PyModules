
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
#? Name:        LV_13_BSIM3v3.py
#? Purpose:     Compute drain current using the BSIM3v3 model
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------

import Log 
from Equations  import Equations
import numpy as np
#? -------------------------------------------------------------------------------

class BSIM3v3Model:
    def __init__(self, param_path=None):
        logger          = Log.Logger()
        self.params     = logger.load_parameters()
        self.eq         = Equations()
        self.mu_0       = self.params["mu0"]["VALUE"]
        self.C_ox       = self.params["C_ox"]["VALUE"]
        self.alpha      = self.params["alpha"]["VALUE"]
        self.theta      = self.params["theta"]["VALUE"]
        self.lambda_    = self.params["lambda_"]["VALUE"]
        self.tox        = self.params["TOX"]["VALUE"]
        self.T          = 300
        
        self.C_g_total  = self.C_ox 
        
    def compute(self, Vgs, Vds,Vsb=0.0,T=300):
        Vth             = self.eq.compute_Vth(Vsb,T)
        Vsat            = Vgs - Vth
        mu_eff          = self.mu_0 / (1 + self.theta * ( Vsat / self.tox))

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
                    Id  = mu_eff * self.C_ox * (1 /1) * ((Vsat * Vds) - 0.5 * Vds ** 2)
                    Cgs = 0.0
                    Cgd = 0.0
                    Cds = 0.0
            case "saturation"   :   
                    Id  = (0.5 * mu_eff * self.C_ox * (1 / 1) * Vsat ** 2 *(1 + self.lambda_ * Vds))
                    Cgs = 0.0
                    Cgd = 0.0
                    Cds = 0.0

        return Id ,Cgs, Cgd, Cds

#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    model               = BSIM3v3Model()
    Vgs , Vds , Vsb ,T  = 15 , 600 , 0.0 , 300
    Id,Cgs, Cgd, Cds    = model.compute(Vgs=Vgs, Vds=Vds,Vsb=Vsb,T=T)
    print("-------------------------------------------------------")
    print(f"\n(Vgs={Vgs}, Vds={Vds}, Vsb={Vsb})")
    print(f"\nID  = {Id:.6e} A")
    print(f"Cgs = {Cgs:.3e} F\nCgd = {Cgd:.3e} F\nCds = {Cds:.3e} F")
    print("-------------------------------------------------------")
#? -------------------------------------------------------------------------------

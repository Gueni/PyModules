
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
        self.C_ox       = self.params["C_ox"]["VALUE"]
        self.alpha      = self.params["alpha"]["VALUE"]
        
        self.C_g_total  = self.C_ox 
        
    def _ID_(self, Vgs, Vds,Vsb=0.0,T=300):
        Vth             = self.eq.compute_Vth(Vsb,T)
        Vsat            = Vgs - Vth
        mu_eff          = self.mu_0 / (1 + self.theta * ( Vsat / self.tox))

        if   Vsat      <= 0     :   region = "cutoff"       #! Vgs <= Vth
        elif Vsat      >= Vds   :   region = "linear"       #! vds <= vgs-Vth
        elif Vsat      <  Vds   :   region = "saturation"   #! Vds >= Vgs - Vth

        match region:
            case "cutoff"       :   Id = 0.0
            case "linear"       :   Id = mu_eff * self.C_ox * (1 /1) * ((Vsat * Vds) - 0.5 * Vds ** 2)
            case "saturation"   :   Id = (0.5 * mu_eff * self.C_ox * (1 / 1) * Vsat ** 2 *(1 + self.lambda_ * Vds))

        return np.float64(Id)

    def _Caps_(self, Vgs, Vds,Vsb=0.0):
        Vth             = self.eq.compute_Vth(Vsb)
        Vsat    = Vgs - Vth

        if      Vsat    <= 0    : # region = "cutoff"       #! Vgs <= Vth
                Cgs = 0.0
                Cgd = 0.0
                Cds = 0.0
        elif    Vsat    >= Vds  : # region = "linear"       #! vds <= vgs-Vth
                Cgs = 0.0
                Cgd = 0.0
                Cds = 0.0
        elif    Vsat    <  Vds  : # region = "saturation"   #! Vds >= Vgs - Vth
                Cgs = 0.0
                Cgd = 0.0
                Cds = 0.0

        return Cgs, Cgd, Cds

#? -------------------------------------------------------------------------------
# if __name__ == "__main__":
#     model           = BSIM3v3Model()
#     Vgs , Vds , Vsb ,T  = 15 , 600 , 1.0 , 300
#     Id                  = model._ID_(Vgs=Vgs, Vds=Vds,Vsb=Vsb,T=T)
#     Cgs, Cgd, Cds       = model._Caps_(Vgs=Vgs, Vds=Vds,Vsb=Vsb)
#     print(f"ID_BSIM3v3(Vgs={Vgs}, Vds={Vds}) = {Id:.6e} A")
#     print(f"Caps (BSIM3v3-like) at Vgs={Vgs}, Vds={Vds}:\n  Cgs = {Cgs:.3e} F\n  Cgd = {Cgd:.3e} F\n  Cds = {Cds:.3e} F")
#? -------------------------------------------------------------------------------

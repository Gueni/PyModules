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
        self.KP         = self.mu * self.C_ox
        self.L_eff      = 1 
        self.W_eff      = 1
        self.alpha      = self.params["alpha"]["VALUE"]
        self.C_g_total  = self.C_ox 

    def _ID_(self, Vgs, Vds, Vsb=0.0):
        Vth             = self.eq.compute_Vth(Vsb)
        Vsat            = Vgs - Vth
        W_over_L        = self.W_eff / self.L_eff

        if   Vsat      <= 0     :   region = "cutoff"       #! Vgs <= Vth
        elif Vsat      >= Vds   :   region = "linear"       #! vds <= vgs-Vth
        elif Vsat      <  Vds   :   region = "saturation"   #! Vds >= Vgs - Vth

        match region:
            case "cutoff"       :   Id = 0.0
            case "linear"       :   Id = self.KP * W_over_L * (1 + self.lambda_ * Vds) * (Vsat - (Vds/2)) * Vds
            case "saturation"   :   Id = 1/2 * self.KP * W_over_L * (1 + self.lambda_ * Vds) * np.square(Vsat)
        return np.float64(Id)

    def _Caps_(self, Vgs, Vds, Vsb=0.0):
        Vth     = self.eq.compute_Vth(Vsb)
        Vsat    = Vgs - Vth

        if      Vsat    <= 0    : # region = "cutoff"       #! Vgs <= Vth
                Cgs = 0.0
                Cgd = 0.0
                Cds = 0.0
        elif    Vsat    >= Vds  : # region = "linear"       #! vds <= vgs-Vth
                Cgs = 2 / 3 * self.C_g_total
                Cgd = 1 / 3 * self.C_g_total
                Cds = 0.0
        elif    Vsat    <  Vds  : # region = "saturation"   #! Vds >= Vgs - Vth
                Cgs = 2 / 3 * self.C_g_total
                Cgd = 0.0
                Cds = 0.0

        return Cgs, Cgd, Cds
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    model           = ShichmanHodgesModel()
    Vgs , Vds , Vsb = 20 , 10 , 1.0
    Id              = model._ID_(Vgs=Vgs, Vds=Vds,Vsb=Vsb)
    Cgs, Cgd, Cds   = model._Caps_(Vgs=Vgs, Vds=Vds,Vsb=Vsb)
    print(f"ID_ShichmanHodges(Vgs={Vgs}, Vds={Vds}, Vsb={Vsb}) = {Id:.6e} A")
    print(f"Caps (Shichman-Hodges) at Vgs={Vgs}, Vds={Vds}:\n  Cgs = {Cgs:.3e} F\n  Cgd = {Cgd:.3e} F\n  Cds = {Cds:.3e} F")
#? -------------------------------------------------------------------------------

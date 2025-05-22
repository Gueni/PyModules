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
from math import sqrt

#? -------------------------------------------------------------------------------
class ShichmanHodgesModel:
    def __init__(self, param_path=None):
        logger          = Log.Logger()
        self.eq         = Equations()
        self.params     = logger.load_parameters()
        self.mu         = self.params["UO"]["VALUE"]               
        self.C_ox       = self.params["COX"]["VALUE"]              
        self.lambda_    = self.params["lambda"]["VALUE"]           
        self.W          = self.params["W"]["VALUE"]                
        self.L          = self.params["L"]["VALUE"]                
        self.KP         = self.mu * self.C_ox  

    def compute_Id(self, Vgs, Vds, Vsb=0.0):
        Vth             = self.eq.compute_Vth(Vsb)
        Vov             = Vgs - Vth
        Vov_clipped     = self.eq.clip(Vov)
        W_over_L        = self.W / self.L

        if   Vov_clipped    <= 0            :   region = "cutoff"
        elif Vds            <= Vov_clipped  :   region = "linear"
        elif Vds            > Vov_clipped   :   region = "saturation"

        match region:
            case "cutoff"       :   Id = 0.0
            case "linear"       :   Id = self.KP * W_over_L * (Vov_clipped * Vds - 0.5 * Vds ** 2)
            case "saturation"   :
                                    Id = 0.5 * self.KP * W_over_L * Vov_clipped ** 2
                                    Id *= (1 + self.lambda_ * Vds)
        return self.eq.clip(Id)
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    model = ShichmanHodgesModel()
    Vgs = 15
    Vds = 600
    Vsb = 0
    Id = model.compute_Id(Vgs, Vds, Vsb)
    print(f"ID_ShichmanHodges(Vgs={Vgs}, Vds={Vds}, Vsb={Vsb}) = {Id:.6e} A")
#? -------------------------------------------------------------------------------

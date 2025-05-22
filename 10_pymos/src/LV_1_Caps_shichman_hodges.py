
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
#? Name:        Caps_shichman_hodges.py
#? Purpose:     Compute intrinsic capacitances using the Shichman-Hodges model
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import Log 
from Equations import Equations
#? -------------------------------------------------------------------------------
class ShichmanHodgesCapacitances:
    def __init__(self):
        logger          = Log.Logger()
        self.params     = logger.load_parameters()
        self.eq         = Equations()
        self.C_ox       = self.params["C_ox"]["VALUE"]                   # Oxide capacitance (F/m²)
        self.Vth        = self.params["Vth"]["VALUE"]                    # Threshold voltage (V), manually defined
        self.alpha      = self.params["alpha"]["VALUE"]                  # Charge partitioning factor
        self.W          = self.params["W"]["VALUE"]                      # Width (m)
        self.L          = self.params["L"]["VALUE"]                      # Length (m)
        self.C_g_total  = self.C_ox * self.W * self.L

    def compute(self, Vgs, Vds):
        V_ov = self.eq.clip(Vgs - self.Vth)

        if V_ov <= 0:
            # Cutoff region
            Cgs = 0.0
            Cgd = 0.0
            Cds = 0.0
        elif Vds < V_ov:
            # Triode region
            Cgs = 2 / 3 * self.C_g_total
            Cgd = 1 / 3 * self.C_g_total
            Cds = 0.0
        else:
            # Saturation region
            Cgs = 2 / 3 * self.C_g_total
            Cgd = 0.0
            Cds = 0.0

        return Cgs, Cgd, Cds
#? -------------------------------------------------------------------------------

if __name__ == "__main__":
    Vgs = 2.0
    Vds = 1.0
    cap_model = ShichmanHodgesCapacitances()
    Cgs, Cgd, Cds = cap_model.compute(Vgs, Vds)
    print(f"Caps (Shichman-Hodges) at Vgs={Vgs}, Vds={Vds}:\n  Cgs = {Cgs:.3e} F\n  Cgd = {Cgd:.3e} F\n  Cds = {Cds:.3e} F")
#? -------------------------------------------------------------------------------
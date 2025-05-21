
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
#? Name:        Caps_BSIM3v3.py
#? Purpose:     Compute BSIM3v3 intrinsic capacitances (Cgs, Cgd, Cds)
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import Log 
from Equations import Equations
#? -------------------------------------------------------------------------------
class BSIM3v3Capacitances:
    def __init__(self):
        logger          = Log.Logger()
        self.params     = logger.load_parameters()

        self.C_ox       = self.params["C_ox"]                   # Oxide capacitance (F/m²)
        self.Vth        = self.params["Vth"]                    # Threshold voltage (V), manually defined
        self.alpha      = self.params["alpha"]                  # Charge partitioning factor
        self.W          = self.params["W"]                      # Width (m)
        self.L          = self.params["L"]                      # Length (m)
        self.C_g_total  = self.C_ox * self.W * self.L
        
    def compute(self, Vgs, Vds):
        V_ov = Equations.clip(Vgs - self.Vth)

        if V_ov <= 0:
            # Cutoff
            Cgs = Cgd = Cds = 0.0
        elif Vds < V_ov:
            # Triode (linear) region
            Cgs = self.alpha * self.C_g_total
            Cgd = (1 - self.alpha) * self.C_g_total
            Cds = 0.0
        else:
            # Saturation region
            Cgs = self.alpha * self.C_g_total
            Cgd = 0.0
            Cds = 0.0

        return Cgs, Cgd, Cds
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    Vgs = 2.0
    Vds = 1.2
    cap_model = BSIM3v3Capacitances()
    Cgs, Cgd, Cds = cap_model.compute(Vgs, Vds)
    print(f"Caps (BSIM3v3-like) at Vgs={Vgs}, Vds={Vds}:\n  Cgs = {Cgs:.3e} F\n  Cgd = {Cgd:.3e} F\n  Cds = {Cds:.3e} F")
#? -------------------------------------------------------------------------------
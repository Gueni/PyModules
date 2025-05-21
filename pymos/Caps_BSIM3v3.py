# D:\WORKSPACE\Python_code\pymos\Caps_BSIM3v3.py

import numpy as np
import json
import os
from Equations import Equations


class BSIM3v3Capacitances:
    def __init__(self):
        self.params = self.load_parameters()
        self.C_ox = 0.02     # Oxide capacitance (F/m²)
        self.W = self.params["W"]           # Width (m)
        self.L = self.params["L"]           # Length (m)
        self.Vth = 0.02                     # Threshold voltage (V), manually defined
        self.alpha = 0.6                    # Charge partitioning factor
        self.C_g_total = self.C_ox * self.W * self.L

    def load_parameters(self):
        path = r'D:\WORKSPACE\Python_code\pymos\vars.json'
        with open(path, "r") as f:
            data = json.load(f)
        return {k: v["value"] for k, v in data.items()}

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


# # Optional test
# if __name__ == "__main__":
#     Vgs = 2.0
#     Vds = 1.2
#     cap_model = BSIM3v3Capacitances()
#     Cgs, Cgd, Cds = cap_model.compute(Vgs, Vds)
#     print(f"Caps (BSIM3v3-like) at Vgs={Vgs}, Vds={Vds}:\n  Cgs = {Cgs:.3e} F\n  Cgd = {Cgd:.3e} F\n  Cds = {Cds:.3e} F")

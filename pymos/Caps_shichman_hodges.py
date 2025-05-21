# D:\WORKSPACE\Python_code\pymos\Caps_shichman_hodges.py

import numpy as np
import json
import os
from Equations import Equations


class ShichmanHodgesCapacitances:
    def __init__(self):
        self.params = self.load_parameters()
        self.C_ox = 0.02
        self.W = self.params["W"]
        self.L = self.params["L"]
        self.Vth = 0.02
        self.C_g_total = self.C_ox * self.W * self.L

    def load_parameters(self):
        path = r'D:\WORKSPACE\Python_code\pymos\vars.json'
        with open(path, "r") as f:
            data = json.load(f)
        return {k: v["value"] for k, v in data.items()}

    def compute(self, Vgs, Vds):
        V_ov = Equations.clip(Vgs - self.Vth)

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


# # Optional test
# if __name__ == "__main__":
#     Vgs = 2.0
#     Vds = 1.0
#     cap_model = ShichmanHodgesCapacitances()
#     Cgs, Cgd, Cds = cap_model.compute(Vgs, Vds)
#     print(f"Caps (Shichman-Hodges) at Vgs={Vgs}, Vds={Vds}:\n  Cgs = {Cgs:.3e} F\n  Cgd = {Cgd:.3e} F\n  Cds = {Cds:.3e} F")

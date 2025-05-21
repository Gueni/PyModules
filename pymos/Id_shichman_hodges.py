# -*- coding: utf-8 -*-

import json
import Equations 


class ShichmanHodgesModel:
    def __init__(self, param_path=None):
        if param_path is None:
            param_path = r'D:\WORKSPACE\Python_code\pymos\vars.json'
        self.params = self._load_parameters(param_path)
        self._extract_params()

    def _load_parameters(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        return {k: v["value"] for k, v in data.items()}

    def _extract_params(self):
        self.mu = 0.02     # Mobility (m^2/Vs)
        self.C_ox = 0.02    # Oxide capacitance (F/m^2)
        self.W = self.params["W"]           # Channel width (m)
        self.L = self.params["L"]           # Channel length (m)
        self.Vth = 1.0                      # Threshold voltage (V)
        self.lambda_ = 0.02                 # Channel-length modulation (1/V)

    def compute_Id(self, Vgs, Vds):
        V_ov = Vgs - self.Vth
        V_ov_clipped = Equations.Equations.clip(V_ov)

        if V_ov_clipped <= 0:
            return 0.0  # Cutoff region

        if Vds < V_ov_clipped:
            # Triode (linear) region
            Id = self.mu * self.C_ox * (self.W / self.L) * (V_ov_clipped * Vds - 0.5 * Vds ** 2)
        else:
            # Saturation region
            Id = 0.5 * self.mu * self.C_ox * (self.W / self.L) * V_ov_clipped ** 2
            Id *= Equations.Equations.channel_length_modulation(self.lambda_, Vds)

        return Equations.Equations.clip(Id)


# Optional test
if __name__ == "__main__":
    model = ShichmanHodgesModel()
    Vgs = 2.0
    Vds = 1.5
    Id = model.compute_Id(Vgs, Vds)
    print(f"ID_ShichmanHodges(Vgs={Vgs}, Vds={Vds}) = {Id:.6e} A")

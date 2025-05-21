# -*- coding: utf-8 -*-
import json
import Equations

class BSIM3v3Model:
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
        self.mu_0 = 0.002         # Low-field mobility (cm^2/Vs)
        self.C_ox = 0.002        # Oxide capacitance (F/m^2)
        self.W = self.params["W"]               # Channel width (m)
        self.L = self.params["L"]               # Channel length (m)
        self.Vth = 0.1                          # Threshold voltage (V)
        self.theta = 0.02                       # Mobility degradation factor
        self.lambda_ = 0.02                     # Channel-length modulation
        self.tox = 0.02           # Oxide thickness (m)
        self.T = self.params.get("T", 300)      # Temperature (K)
        
    def compute_Id(self, Vgs, Vds):
        Vt = Equations.Equations.thermal_voltage(self.T)
        V_ov = Equations.Equations.surface_potential(self.Vth, Vgs)
        V_ov_clipped = Equations.Equations.clip(V_ov)

        # Effective mobility
        E_eff = V_ov_clipped / self.tox
        mu_eff = Equations.Equations.effective_mobility(self.mu_0, E_eff, self.theta)

        # Saturation voltage
        Vdsat = Equations.Equations.saturation_voltage(Vgs, self.Vth)

        if Vds < Vdsat:
            # Linear region
            Id = mu_eff * self.C_ox * (self.W / self.L) * ((V_ov_clipped * Vds) - 0.5 * Vds ** 2)
        else:
            # Saturation region
            Id = 0.5 * mu_eff * self.C_ox * (self.W / self.L) * V_ov_clipped ** 2
            Id *= Equations.Equations.channel_length_modulation(self.lambda_, Vds)

        return Equations.Equations.clip(Id)


# Optional test/demo
if __name__ == "__main__":
    model = BSIM3v3Model()
    Vgs = 1.8
    Vds = 1.2
    Id = model.compute_Id(Vgs, Vds)
    print(f"ID_BSIM3v3(Vgs={Vgs}, Vds={Vds}) = {Id:.6e} A")

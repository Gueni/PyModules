
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
#? Name:        Id_BSIM3v3.py
#? Purpose:     Compute drain current using the BSIM3v3 model
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------

import Log 
from Equations  import Equations
#? -------------------------------------------------------------------------------

class BSIM3v3Model:
    def __init__(self, param_path=None):
        logger          = Log.Logger()
        self.params          = logger.load_parameters()
        self.eq         = Equations()
        self.mu_0       = self.params["mu0"]["VALUE"] # Convert to m^2/Vs
        self.C_ox       = self.params["C_ox"]["VALUE"]                   # Oxide capacitance (F/m²)
        self.alpha      = self.params["alpha"]["VALUE"]                  # Charge partitioning factor
        self.W          = self.params["W"]["VALUE"]               # Channel width (m)
        self.L          = self.params["L"]["VALUE"]               # Channel length (m)
        self.theta      = self.params["theta"]["VALUE"]               # Channel length (m)
        self.lambda_    = self.params["lambda_"]["VALUE"]               # Channel length (m)
        self.tox        = self.params["tox"]["VALUE"]               # Channel length (m)
        self.T          = 300                               # Temperature (K)
        
    def compute_Id(self, Vgs, Vds):

        Vt = self.eq.thermal_voltage(self.T)
        V_ov = self.eq.surface_potential(Vt, Vgs)
        V_ov_clipped = self.eq.clip(V_ov)

        # Effective mobility
        E_eff = V_ov_clipped / self.tox
        mu_eff = self.eq.effective_mobility(self.mu_0, E_eff, self.theta)

        # Saturation voltage
        Vdsat = self.eq.saturation_voltage(Vgs, Vt)

        if Vds < Vdsat:
            # Linear region
            Id = mu_eff * self.C_ox * (self.W / self.L) * ((V_ov_clipped * Vds) - 0.5 * Vds ** 2)
        else:
            # Saturation region
            Id = 0.5 * mu_eff * self.C_ox * (self.W / self.L) * V_ov_clipped ** 2
            Id *= self.eq.channel_length_modulation(self.lambda_, Vds)

        return self.eq.clip(Id)

#? -------------------------------------------------------------------------------

if __name__ == "__main__":
    model = BSIM3v3Model()
    Vgs = 15
    Vds = 600
    Id = model.compute_Id(Vgs, Vds)
    print(f"ID_BSIM3v3(Vgs={Vgs}, Vds={Vds}) = {Id:.6e} A")
#? -------------------------------------------------------------------------------

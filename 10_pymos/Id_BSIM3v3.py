
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
import Equations
#? -------------------------------------------------------------------------------

class BSIM3v3Model:
    def __init__(self, param_path=None):
        logger          = Log.Logger()
        self.params          = logger.load_parameters()

        self.mu_0       = self.params["mu0"] * 1e-4  # Convert to m^2/Vs
        self.C_ox       = self.params["C_ox"]                   # Oxide capacitance (F/m²)
        self.alpha      = self.params["alpha"]                  # Charge partitioning factor
        self.W          = self.params["W"]               # Channel width (m)
        self.L          = self.params["L"]               # Channel length (m)
        self.theta      = self.params["theta"]               # Channel length (m)
        self.lambda_    = self.params["lambda_"]               # Channel length (m)
        self.tox        = self.params["tox"]               # Channel length (m)
        self.T          = 300                               # Temperature (K)
        
    def compute_Id(self, Vgs, Vds):

        Vt = Equations.Equations.thermal_voltage(self.T)
        V_ov = Equations.Equations.surface_potential(Vt, Vgs)
        V_ov_clipped = Equations.Equations.clip(V_ov)

        # Effective mobility
        E_eff = V_ov_clipped / self.tox
        mu_eff = Equations.Equations.effective_mobility(self.mu_0, E_eff, self.theta)

        # Saturation voltage
        Vdsat = Equations.Equations.saturation_voltage(Vgs, Vt)

        if Vds < Vdsat:
            # Linear region
            Id = mu_eff * self.C_ox * (self.W / self.L) * ((V_ov_clipped * Vds) - 0.5 * Vds ** 2)
        else:
            # Saturation region
            Id = 0.5 * mu_eff * self.C_ox * (self.W / self.L) * V_ov_clipped ** 2
            Id *= Equations.Equations.channel_length_modulation(self.lambda_, Vds)

        return Equations.Equations.clip(Id)

#? -------------------------------------------------------------------------------

if __name__ == "__main__":
    model = BSIM3v3Model()
    Vgs = 15
    Vds = 600
    Id = model.compute_Id(Vgs, Vds)
    print(f"ID_BSIM3v3(Vgs={Vgs}, Vds={Vds}) = {Id:.6e} A")
#? -------------------------------------------------------------------------------

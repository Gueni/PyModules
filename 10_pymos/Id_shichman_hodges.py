
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
import Equations
#? -------------------------------------------------------------------------------
class ShichmanHodgesModel:
    def __init__(self, param_path=None):
        logger          = Log.Logger()
        self.params          = logger.load_parameters()

        self.mu         = self.params["mu_exp"] * 1e-4  # Convert to m^2/Vs
        self.C_ox       = self.params["C_ox"]                   # Oxide capacitance (F/m²)
        self.Vth        = self.params["Vth"]                    # Threshold voltage (V), manually defined
        self.alpha      = self.params["alpha"]                  # Charge partitioning factor
        self.W          = self.params["W"]               # Channel width (m)
        self.L          = self.params["L"]               # Channel length (m)
        self.theta      = self.params["theta"]               # Channel length (m)
        self.lambda_    = self.params["lambda_"]               # Channel length (m)
        self.tox        = self.params["tox"]               # Channel length (m)
        self.T          = 300                               # Temperature (K)

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

#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    model = ShichmanHodgesModel()
    Vgs = 15
    Vds = 600
    Id = model.compute_Id(Vgs, Vds)
    print(f"ID_ShichmanHodges(Vgs={Vgs}, Vds={Vds}) = {Id:.6e} A")
#? -------------------------------------------------------------------------------
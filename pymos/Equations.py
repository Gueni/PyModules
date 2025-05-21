
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
#? Name:        Equations.py
#? Purpose:     Define shared sub-equations used across current and capacitance models
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import Log 
import numpy as np
#? -------------------------------------------------------------------------------
class Equations:
    logger          = Log.Logger()
    params          = logger.load_parameters()
    q               = params["q"]                   # Oxide capacitance (F/m²)
    k               = params["k"]                   # Boltzmann constant (J/K)
    eps_0           = params["eps_ox"]             # Oxide permittivity (F/m)
    T_default       = 300               # Default temperature (K)

    @staticmethod
    def thermal_voltage(T=T_default):
        return Equations.k * T / Equations.q

    @staticmethod
    def effective_mobility(mu_0, E_eff, theta):
        return mu_0 / (1 + theta * E_eff)

    @staticmethod
    def surface_potential(Vth, Vgs):
        return Vgs - Vth

    @staticmethod
    def saturation_voltage(Vgs, Vth):
        return Vgs - Vth

    @staticmethod
    def channel_length_modulation(lambda_, Vds):
        return 1 + lambda_ * Vds

    @staticmethod
    def compute_capacitance(C_ox, W, L, factor=1.0):
        return factor * C_ox * W * L

    @staticmethod
    def compute_e_eff(Vgs, Vth, tox):
        return (Vgs - Vth) / tox  # Very simplified

    @staticmethod
    def compute_C_ox(eps_ox, tox):
        return eps_ox / tox

    @staticmethod
    def diode_eq(V, Is, n=1, T=T_default):
        Vt = Equations.thermal_voltage(T)
        return Is * (np.exp(V / (n * Vt)) - 1)

    @staticmethod
    def clip(value, min_val=0):
        return np.maximum(value, min_val)
#? -------------------------------------------------------------------------------
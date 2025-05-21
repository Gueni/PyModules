# D:\WORKSPACE\Python_code\pymos\Equations.py

import numpy as np

class Equations:
    # Physical constants
    q = 1.602e-19       # Elementary charge (C)
    k = 1.381e-23       # Boltzmann constant (J/K)
    eps_0 = 8.854e-12   # Vacuum permittivity (F/m)
    T_default = 300     # Default temperature (K)

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


# Optional demo
if __name__ == "__main__":
    T = 300
    Vt = Equations.thermal_voltage(T)
    print(f"Thermal voltage at {T}K: {Vt:.3e} V")

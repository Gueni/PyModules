
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
    eps_0           = params["eps_ox"]              # Oxide permittivity (F/m)
    eps_sic         = params['eps_sic']             # Permittivity of SiC
    Nsurf           = params['Nsurf']               # Surface doping concentration
    VFB             = params['VFB']                 # Flatband voltage
    Vsurf           = params['Vsurf']               # Surface transition voltage
    mjsurf          = params['mjsurf']              # Surface grading coefficient
    ni              = params['ni']                  # Intrinsic carrier concentration
    PPW             = params['PPW']                 # P-well doping concentration
    tox             = params['tox']                 # Oxide thickness
    mu              = params['mu']                  # Mobility
    NJFET           = params['NJFET']               # JFET doping concentration 
    H_by_eff        = params['H_by_eff']            # Effective height
    XJPW            = params['XJPW']                # Junction depth
    dpw             = params['dpw']                 # P-well separation
    mj              = params['mj']                  # Surface grading coefficient
    T_default       = 300                           # Default temperature (K)

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
    @staticmethod
    def phi_t(T):
        phi = (Equations.k * T) / Equations.q
        return phi

    def phi(T):#* Calculate the potential barrier at temperature T
        return Equations.phi_t(T) * np.log(Equations.NJFET * Equations.PPW / (Equations.ni**2))

    def alpha():#* Calculate the depletion factor
        return np.sqrt((2 * Equations.eps_sic * Equations.PPW) / (Equations.q * Equations.NJFET * (Equations.NJFET + Equations.PPW)))

    def VTO_func(T): # * Calculate the threshold voltage at temperature T
        return float(Equations.phi(T) - (Equations.dpw / (2 * Equations.alpha()))**2)

    def rho(): #* Calculate the resistivityas a function of mobility mu
        return 1 / (Equations.q * Equations.NJFET * Equations.mu)

    def beta_func(T):#* Calculate the transconductance parameter
        beta     = ((2 * Equations.H_by_eff) / (Equations.XJPW * Equations.rho() *  (- Equations.VTO_func(T))) ) * ((Equations.dpw/2)-Equations.alpha()*np.sqrt(Equations.phi(T)))
        return float(beta) 

    def Cox():#* Calculate the oxide capacitance
        return Equations.eps_ox / Equations.tox

    def Wdep1_num(VDS_val, VGS_val):#* Calculate the depletion width for the first region
        return np.sqrt((2 * Equations.eps_sic) / (Equations.q * Equations.Nsurf) * min(VDS_val - VGS_val - Equations.VFB, Equations.Vsurf)**Equations.mjsurf)

    def Wdep2_num(VDS_val, VGS_val, T_val):#* Calculate the depletion width for the second region
        return np.sqrt((2 * Equations.eps_sic) / (Equations.q * Equations.Nsurf) * min(VDS_val - VGS_val - Equations.VFB - Equations.Vsurf, Equations.phi(T_val) - Equations.VTO_func(T_val))**Equations.mj)

    def Cdep_num(VDS_val, VGS_val, T_val): #* Calculate the depletion capacitance
        return Equations.eps_sic / ((Equations.Wdep1_num(VDS_val, VGS_val) + Equations.Wdep2_num(VDS_val, VGS_val, T_val)))

#? -------------------------------------------------------------------------------

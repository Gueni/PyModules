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
    def __init__(self):
        self.logger     = Log.Logger()
        self.params     = self.logger.load_parameters()

        self.q          = self.params["q"]["VALUE"]
        self.k          = self.params["k"]["VALUE"]
        self.eps_ox     = self.params["eps_ox"]["VALUE"]
        self.eps_sic    = self.params["eps_sic"]["VALUE"]
        self.Nsurf      = self.params["Nsurf"]["VALUE"]
        self.VFB        = self.params["VFB"]["VALUE"]
        self.Vsurf      = self.params["Vsurf"]["VALUE"]
        self.mjsurf     = self.params["mjsurf"]["VALUE"]
        self.ni         = self.params["ni"]["VALUE"]
        self.PPW        = self.params["PPW"]["VALUE"]
        self.tox        = self.params["tox"]["VALUE"]
        self.mu         = self.params["mu"]["VALUE"]
        self.NJFET      = self.params["NJFET"]["VALUE"]
        self.H_by_eff   = self.params["H_by_eff"]["VALUE"]
        self.XJPW       = self.params["XJPW"]["VALUE"]
        self.dpw        = self.params["dpw"]["VALUE"]
        self.mj         = self.params["mj"]["VALUE"]
        self.T_default  = 300

    def thermal_voltage(self, T=None):
        if T is None:
            T = self.T_default
        return self.k * T / self.q

    def effective_mobility(self, mu_0, E_eff, theta):
        return mu_0 / (1 + theta * E_eff)

    def surface_potential(self, Vth, Vgs):
        return Vgs - Vth

    def saturation_voltage(self, Vgs, Vth):
        return Vgs - Vth

    def channel_length_modulation(self, lambda_, Vds):
        return 1 + lambda_ * Vds

    def compute_capacitance(self, C_ox, W, L, factor=1.0):
        return factor * C_ox * W * L

    def compute_e_eff(self, Vgs, Vth):
        return (Vgs - Vth) / self.tox  # Simplified

    def compute_C_ox(self):
        return self.eps_ox / self.tox

    def diode_eq(self, V, Is, n=1, T=None):
        if T is None:
            T = self.T_default
        Vt = self.thermal_voltage(T)
        return Is * (np.exp(V / (n * Vt)) - 1)

    def clip(self, value, min_val=0):
        return np.maximum(value, min_val)

    def phi_t(self, T):
        return (self.k * T) / self.q

    def phi(self, T):
        return self.phi_t(T) * np.log(self.NJFET * self.PPW / (self.ni ** 2))

    def alpha(self):
        return np.sqrt((2 * self.eps_sic * self.PPW) / (self.q * self.NJFET * (self.NJFET + self.PPW)))

    def VTO_func(self, T):
        return float(self.phi(T) - (self.dpw / (2 * self.alpha()))**2)

    def rho(self):
        return 1 / (self.q * self.NJFET * self.mu)

    def beta_func(self, T):
        return float(((2 * self.H_by_eff) / (self.XJPW * self.rho() * (-self.VTO_func(T)))) *
                     ((self.dpw / 2) - self.alpha() * np.sqrt(self.phi(T))))

    def COX(self):
        return self.eps_ox / self.tox

    def Wdep1_num(self, VDS_val, VGS_val):
        return np.sqrt((2 * self.eps_sic) / (self.q * self.Nsurf) *
                       min(VDS_val - VGS_val - self.VFB, self.Vsurf) ** self.mjsurf)

    def Wdep2_num(self, VDS_val, VGS_val, T_val):
        return np.sqrt((2 * self.eps_sic) / (self.q * self.Nsurf) *
                       min(VDS_val - VGS_val - self.VFB - self.Vsurf, self.phi(T_val) - self.VTO_func(T_val)) ** self.mj)

    def Cdep_num(self, VDS_val, VGS_val, T_val):
        return self.eps_sic / (self.Wdep1_num(VDS_val, VGS_val) + self.Wdep2_num(VDS_val, VGS_val, T_val))

    def compute_Vth(self, Vsb):
        return self.params["VTO"]["VALUE"] + self.params["GAMMA"]["VALUE"] * (
            np.sqrt(abs(Vsb + self.params["PHI"]["VALUE"])) - np.sqrt(abs(self.params["PHI"]["VALUE"]))
        )

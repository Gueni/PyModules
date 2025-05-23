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
        self.tox        = self.params["TOX"]["VALUE"]
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

    def compute_Vth(self, Vsb,T=300):
        vbi             = self.params["VTo"]["VALUE"] - self.params["GAMMA"]["VALUE"] *   np.sqrt(self.phi(T)) 
        if      Vsb < 0 :
                vth     = vbi + self.params["GAMMA"]["VALUE"] * ( np.sqrt(self.phi(T)) + 1/2 * (Vsb/np.sqrt(self.phi(T))))
        elif    Vsb >= 0:
                vth     = vbi + self.params["GAMMA"]["VALUE"] *   np.sqrt( self.phi(T)+ Vsb)
        return  vth
    
#? -------------------------------------------------------------------------------

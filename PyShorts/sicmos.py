# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sympy import symbols, Eq, init_printing, sqrt, Min

from rich.table import Table
from rich.console import Console

# --- Constants ---
q = 1.6e-19           # Charge [C]
k = 1.38e-23          # Boltzmann constant [J/K]
eps_sic = 9.7e-13     # SiC permittivity [F/cm]
eps_ox = 3.45e-13     # SiO2 permittivity [F/cm]
tox = 5e-7            # Oxide thickness [cm]
ni = 1.5e10           # Intrinsic carrier concentration [1/cm^3]
PPW = 1e17            # P-well doping [1/cm^3]
NJFET = 1e16          # Jfet doping [1/cm^3]
Nsurf = 1e17           # Surface doping [1/cm^3]
XJPW = 1e-5           # Junction depth [cm]
dpw = 1e-4            # P-well separation [cm]
mu = 100              # Mobility [cm^2/Vs]
H_by_eff = 1e-3       # Effective height [cm]
VFB = -1              # Flatband voltage [V]
Vsurf = 2             # Surface transition voltage [V]
mjsurf = 0.5
mj = 0.5
Cj0 = 1e-12           # Junction capacitance at 0V [F]
Vj = 0.7              # Junction potential [V]
m = 0.5               # CDS grading coefficient
C_overlap = 1e-12     # CGS overlap cap [F]
lambda_ = 0.02        # Channel-length modulation

# --- SymPy setup ---
init_printing(use_unicode=True)

# --- Numerical functions ---

def phi_t(T):
    """Thermal voltage in Volts"""
    return k * T / q

def phi(T):
    """Potential function"""
    # Use max to prevent log of zero or negative
    val = NJFET * PPW / (ni**2)
    if val <= 0:
        return 0.7  # fallback typical value
    return phi_t(T) * np.log(val)

def alpha():
    return np.sqrt((2 * eps_sic * PPW) / (q * NJFET * (NJFET + PPW)))

def VTO_func(T):
    """Threshold voltage"""
    # Calculate alpha once
    a = alpha()
    val = phi(T) - (q * NJFET / (2 * eps_sic)) * (dpw / (2 * a))**2
    # Clamp VTO to reasonable range to avoid negative or zero values causing issues downstream
    return float(val)

def rho():
    return 1 / (q * NJFET * mu)

def beta_func(T):
    """Calculate beta parameter"""
    VTO_val = VTO_func(T)
    phi_val = phi(T)
    delta = phi_val - VTO_val

    # Avoid division by zero or negative delta causing huge beta
    if delta <= 0:
        delta = 0.1  # minimal positive value to keep stable

    val = (2 * H_by_eff) / (XJPW * rho() * delta) * (2 * alpha() / dpw)**2
    return float(val) #/ 1000  # scale down beta by 1000 for testing


def ID(VGS_val, VDS_val, T_val):
    """Calculate drain current"""
    beta_val = beta_func(T_val)
    VTO_val = VTO_func(T_val)
    # Ensure VGS >= VTO to avoid negative current (cutoff region)
    VGS_eff = max(VGS_val - VTO_val, 0)
    Id = beta_val * (2 * VGS_eff - VDS_val) * VDS_val * (1 + lambda_ * VDS_val)
    # Limit negative or extreme values
    if Id < 0:
        return 0.0
    if Id > 1e4:  # cap unrealistically high currents
        return 1e4
    return Id

def Cox():
    return eps_ox / tox

def Wdep1_num(VDS_val, VGS_val):
    return np.sqrt((2 * eps_sic) / (q * Nsurf) * min(VDS_val - VGS_val - VFB, Vsurf)**mjsurf)

def Wdep2_num(VDS_val, VGS_val, T_val):
    return np.sqrt((2 * eps_sic) / (q * Nsurf) * min(VDS_val - VGS_val - VFB - Vsurf, phi(T_val) - VTO_func(T_val))**mj)

def Cdep_num(VDS_val, VGS_val, T_val):
    return eps_sic / (Wdep1_num(VDS_val, VGS_val) + Wdep2_num(VDS_val, VGS_val, T_val))

def CGD_num(VDS_val, VGS_val, T_val):
    Cox_val = Cox()
    Cdep_val = Cdep_num(VDS_val, VGS_val, T_val)
    return (Cox_val * Cdep_val) / (Cox_val + Cdep_val)

def CGS_num(VGS_val):
    return 2e-12 * (VGS_val > 0) + C_overlap

def CDS_num(VDS_val):
    return Cj0 * (1 + VDS_val / Vj)**(-m)

# --- Sweep table generation ---
vds_vals = np.linspace(100, 600, 3)
vgs_vals = np.linspace(10, 20, 3)
temps_C = np.array([25, 75, 125])
temps_K = temps_C + 273.15

table = []
for T, T_C in zip(temps_K, temps_C):
    for VDS_val in vds_vals:
        for VGS_val in vgs_vals:
            table.append({
                "VDS (V)": VDS_val,
                "VGS (V)": VGS_val,
                "Temp (°C)": T_C,
                "ID (A)": ID(VGS_val, VDS_val, T),
                "CGD (nF)": CGD_num(VDS_val, VGS_val, T) * 1e9,
                "CGS (pF)": CGS_num(VGS_val) * 1e12,
                "CDS (fF)": CDS_num(VDS_val) * 1e15
            })
        

df = pd.DataFrame(table).round(3)

# --- Print parameters table with rich ---
params = [
    ("q (elementary charge)", f"{q:.2e}", "C", "Constant"),
    ("k (Boltzmann constant)", f"{k:.2e}", "J/K", "Constant"),
    ("ε_SiC (permittivity SiC)", f"{eps_sic:.2e}", "F/cm", "Datasheet"),
    ("ε_ox (permittivity SiO2)", f"{eps_ox:.2e}", "F/cm", "Datasheet"),
    ("t_ox (oxide thickness)", f"{tox:.2e}", "cm", "Process parameter"),
    ("n_i (intrinsic carrier)", f"{ni:.2e}", "1/cm^3", "Literature"),
    ("N_PW (P-well doping)", f"{PPW:.2e}", "1/cm^3", "Process parameter"),
    ("N_JFET (JFET doping)", f"{NJFET:.2e}", "1/cm^3", "Process parameter"),
    ("μ (mobility)", f"{mu:.1f}", "cm^2/Vs", "Literature"),
    ("H_by_eff (effective height)", f"{H_by_eff:.2e}", "cm", "Device geometry"),
    ("V_FB (flatband voltage)", f"{VFB:.2f}", "V", "Measured"),
    ("V_surf (surface voltage)", f"{Vsurf:.2f}", "V", "Measured"),
    ("m_j_surf (grading coefficient)", f"{mjsurf:.2f}", "-", "Literature"),
    ("C_j0 (junction capacitance)", f"{Cj0:.2e}", "F", "Datasheet"),
    ("V_j (junction potential)", f"{Vj:.2f}", "V", "Datasheet"),
    ("m (grading coefficient CDS)", f"{m:.2f}", "-", "Literature"),
    ("C_overlap (overlap capacitance)", f"{C_overlap:.2e}", "F", "Process"),
    ("λ (channel-length modulation)", f"{lambda_:.2f}", "-", "Literature"),
]

console = Console()
param_table = Table(title="Device Parameters")

param_table.add_column("Parameter", style="cyan")
param_table.add_column("Value", justify="right")
param_table.add_column("Unit", justify="center")
param_table.add_column("Source", style="magenta")

for p, v, u, s in params:
    param_table.add_row(p, v, u, s)
    print(f"T={T:.1f}K, beta={beta_func(T):.3e}, VTO={VTO_func(T):.3f} V")


console.print(param_table)

# --- Save CSV ---
csv_path = "PyShorts/DATA/VDS_VGS_T_Sweep_ID_CGD_CGS_CDS.csv"
df.to_csv(csv_path, index=False)
print(f"\nSweep data saved to {csv_path}")

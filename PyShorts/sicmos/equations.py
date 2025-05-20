
#? Typical Value Range : 
#  vds    = 650 to 1700 V
#  vgs    = -5.0 to +18 V recommended : 0.0 to +20 V
#  Ids    = 10 to 100 A
#  Ciss   = Cgs + Cgd = 1200 to 2500 pF
#  Coss   = Cds + Cgd = 80 to 200 pF
#  Crss   = Cgd = 20 to 50 pF 
#!/usr/bin/env python3
"""
BSIM3-inspired SiC MOSFET model ― compact, commented, and self-documenting
=========================================================================

Implements:
    • Temperature-dependent threshold voltage (body effect + DIBL)
    • Temperature-dependent effective mobility
    • Linear / velocity-saturated / saturation drain current
    • Channel-length modulation
    • Simple Meyer-like gate capacitances (Cgs, Cgd) + junction Cds
    • Pretty console header (rich) and CSV export of sweep results
    • Optional Matplotlib visualisation

Author : <your-name>
Date   : 20 May 2025
"""

# ────────────────────────────────────────────────────────────────────────────────
# Standard & scientific imports
# ────────────────────────────────────────────────────────────────────────────────
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console

# ────────────────────────────────────────────────────────────────────────────────
# I/O helpers
# ────────────────────────────────────────────────────────────────────────────────
def load_params_from_json(json_path: str):
    """
    Read parameter values and meta-data from a JSON file.
    The JSON structure is assumed to be
    {
        "PARAM1": {"value": 1.23, "unit": "...", "equation": "...", ...},
        "PARAM2": {...}
    }
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    params = {k: v["value"] for k, v in data.items()}
    meta   = {k: {kk: vv for kk, vv in v.items() if kk != "value"} for k, v in data.items()}
    return params, meta


def pretty_header(params: dict, meta: dict, log_file_path: str):
    """
    Pretty-print parameter table to terminal & log-file using Rich.
    """
    table = Table(title="MOSFET Model Parameters", show_lines=True)
    table.add_column("Symbol")
    table.add_column("Value")
    table.add_column("Unit")
    table.add_column("Description / Origin")

    for k, m in meta.items():
        val = params.get(k, "—")
        if isinstance(val, float):
            val = f"{val:.4g}"
        table.add_row(k, str(val), m.get("unit", ""), m.get("description", ""))

    con = Console(record=True, color_system=None, force_terminal=True, width=110)
    con.print(table)
    with open(log_file_path, "w", encoding="utf-8") as fh:
        fh.write(con.export_text())


# ────────────────────────────────────────────────────────────────────────────────
# Core physical model
# ────────────────────────────────────────────────────────────────────────────────
def mosfet_model(
    Vgs: float, Vds: float, Vsb: float, T: float, p: dict
):
    """
    Compute I_D, C_gs, C_gd, C_ds for a single bias/temperature point.

    Major equations (also echoed by print_equations):
    ① Threshold voltage with body effect & DIBL:
       Vth = Vth0 + γ(√|2φ_F + V_SB| − √|2φ_F|) − k_T (T−T0) − η V_DS
    ② Effective mobility:
       μ_eff = μ_0 (T0/T)^μ_exp  / (1 + θ1 V_GT + θ2 V_DS)
    ③ Velocity-saturation drain current limit (McKelvey-Canali style):
       V_Dsat = V_GT · L_eff / (V_sat · (1 + α_sat V_GT))
    ④ I_D (linear if V_DS < V_Dsat, else saturation with λ CLM)
    ⑤ Meyer C_gs / C_gd partition; junction C_ds (reverse-biased Cj0 law)
    """

    # ── Temperature-adjusted / auxiliary variables ────────────────────────────
    T0        = 300.0                                # Reference temperature [K]
    kT        = p["kT"]                              # dVth/dT [V / K]
    phi_F     = p["phiF"]                            # Fermi potential [V]
    gamma     = p["gamma"]                           # Body-effect coeff √V
    eta       = p["eta"]                             # DIBL coefficient [-]
    Vth0      = p["Vth0"]                            # Nominal Vth at T0, Vsb=0, Vds≈0
    mu0       = p["mu0"]                             # Low-field mobility at T0
    mu_exp    = p["mu_exp"]                          # Temperature exponent
    theta1    = p["theta1"]                          # Mobility degradation w/ V_GT
    theta2    = p["theta2"]                          # Mobility degradation w/ V_DS
    Vsat      = p["Vsat"]                            # Saturation velocity [m/s]
    alpha_sat = p["alpha_sat"]                       # Field-induced Vsat roll-off
    CLM_lambda= p["lambda"]                          # Channel-length modulation
    Cox       = p["Cox"]                             # Gate oxide capacitance F/m²
    W, L      = p["W"], p["L"]                       # Device dimensions [m]
    Cj0, Vbi, m = p["Cj0"], p["Vbi"], p["m"]         # Junction capacitance params

    # ── Fundamental charges/voltages ──────────────────────────────────────────
    V_FB      = .01                            # (Needed if φ_F and γ derived)
    Vth_body  = Vth0 + gamma*(np.sqrt(np.abs(2*phi_F + Vsb))
                              - np.sqrt(np.abs(2*phi_F)))
    Vth_temp  = Vth_body - kT*(T - T0)               # Temperature shift
    Vth       = Vth_temp - eta * Vds                 # DIBL shift

    Vgt       = Vgs - Vth                            # Gate overdrive
    if Vgt <= 0:
        # ── Cutoff region ────────────────────────────────────────────────────
        return dict(Id=0.0, Cgs=0.0, Cgd=0.0, Cds=Cj0)

    # ── Mobility (Philips / BSIM3 style) ──────────────────────────────────────
    mu_eff = mu0 * (T0 / T) ** mu_exp
    mu_eff /= (1.0 + theta1 * Vgt + theta2 * Vds)

    # ── Velocity-saturation critical V_DSsat ─────────────────────────────────
    L_eff    = L                                     # (No ΔL modelling here)
    V_Dsat   = Vgt * L_eff / (Vsat * (1.0 + alpha_sat * Vgt))

    # ── Drain current calculation ────────────────────────────────────────────
    if Vds < V_Dsat:
        # Linear (triode) or velocity-saturated – gradual channel approximation
        Id = mu_eff * Cox * (W/L_eff) * (Vgt * Vds - 0.5 * Vds**2)
    else:
        # Saturation with CLM
        Id_sat = 0.5 * mu_eff * Cox * (W/L_eff) * Vgt**2
        Id = Id_sat * (1.0 + CLM_lambda * (Vds - V_Dsat))

    # ── Capacitances (simplified Meyer) ──────────────────────────────────────
    # Gate charge splits 2:1 between source and drain at V_ds < V_Dsat,
    # Cgd pinches off in saturation.
    if Vds < V_Dsat:
        Cgs = (2.0/3.0) * Cox * W * L_eff
        Cgd = (1.0/3.0) * Cox * W * L_eff
    else:
        Cgs = (2.0/3.0) * Cox * W * L_eff * 0.5   # half because Q-channel taper
        Cgd = 0.0

    # Drain-substrate depletion capacitance
    Cds = Cj0 / (1.0 + max(Vds, 0) / Vbi) ** m

    return dict(Id=Id, Cgs=Cgs, Cgd=Cgd, Cds=Cds)


# ────────────────────────────────────────────────────────────────────────────────
# Parameter sweep & plotting utilities
# ────────────────────────────────────────────────────────────────────────────────
def sweep_and_plot(
    Vgs_vals, Vds_vals, T_vals, params, csv_path="results.csv", show=True
):
    """
    Sweep VGS, VDS, and temperature; save CSV; optionally plot key curves.
    """
    records = []
    for T in T_vals:
        for Vgs in Vgs_vals:
            for Vds in Vds_vals:
                out = mosfet_model(Vgs, Vds, Vsb=0.0, T=T, p=params)
                records.append(
                    dict(T=T, Vgs=Vgs, Vds=Vds,
                         Id=out["Id"], Cgs=out["Cgs"],
                         Cgd=out["Cgd"], Cds=out["Cds"])
                )

    df = pd.DataFrame.from_records(records)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)

    if not show:
        return

    # ─── Simple visualisation ────────────────────────────────────────────────
    fig, axs = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("MOSFET BSIM3-like Characteristics", fontsize=14)

    # I-V: Id vs Vgs @ fixed Vds
    for vds in np.unique(df["Vds"]):
        sel = (df["Vds"] == vds) & (df["T"] == T_vals[-1])
        axs[0, 0].plot(df["Vgs"][sel], df["Id"][sel], label=f"Vds={vds:g} V")
    axs[0, 0].set(xlabel="Vgs [V]", ylabel="Id [A]", title="Id–Vgs")
    axs[0, 0].legend(), axs[0, 0].grid(True)

    # I-V: Id vs Vds @ fixed Vgs
    for vgs in np.unique(df["Vgs"]):
        sel = (df["Vgs"] == vgs) & (df["T"] == T_vals[-1])
        axs[0, 1].plot(df["Vds"][sel], df["Id"][sel], label=f"Vgs={vgs:g} V")
    axs[0, 1].set(xlabel="Vds [V]", ylabel="Id [A]", title="Id–Vds")
    axs[0, 1].legend(), axs[0, 1].grid(True)

    # Capacitances vs Vds
    sel = (df["Vgs"] == Vgs_vals[len(Vgs_vals)//2]) & (df["T"] == T_vals[-1])
    axs[1, 0].plot(df["Vds"][sel], df["Cgs"][sel], label="Cgs")
    axs[1, 0].plot(df["Vds"][sel], df["Cgd"][sel], label="Cgd")
    axs[1, 0].plot(df["Vds"][sel], df["Cds"][sel], label="Cds")
    axs[1, 0].set(xlabel="Vds [V]", ylabel="Capacitance [F]", title="C–V")
    axs[1, 0].legend(), axs[1, 0].grid(True)

    # Id vs Temperature at a large Vds & Vgs
    sel = (df["Vgs"] == max(Vgs_vals)) & (df["Vds"] == max(Vds_vals))
    axs[1, 1].plot(df["T"][sel], df["Id"][sel])
    axs[1, 1].set(xlabel="Temperature [K]", ylabel="Id [A]",
                  title=f"Id vs T @ Vgs={max(Vgs_vals)} V, Vds={max(Vds_vals)} V")
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()


# ────────────────────────────────────────────────────────────────────────────────
# Equation echo -- run once so user sees formulas at runtime
# ────────────────────────────────────────────────────────────────────────────────
def print_equations():
    """
    Dump all governing equations to the console in plain ASCII.
    """
    eqs = [
        "Threshold voltage (body effect + DIBL + temp):",
        "  Vth = Vth0 + γ(√|2φ_F + V_SB| − √|2φ_F|)  −  k_T (T − T0)  −  η V_DS",
        "",
        "Effective mobility (temperature & vertical-field dependent):",
        "  μ_eff = μ_0 (T0/T)^μ_exp  / [1 + θ1 V_GT + θ2 V_DS]",
        "",
        "Velocity-saturation drain-to-source voltage limit:",
        "  V_Dsat = V_GT · L_eff / (V_sat (1 + α_sat V_GT))",
        "",
        "Drain current:",
        "  If V_DS < V_Dsat:",
        "      I_D = μ_eff C_ox (W/L) ( V_GT V_DS − 0.5 V_DS² )",
        "  Else (saturation):",
        "      I_Dsat = 0.5 μ_eff C_ox (W/L) V_GT²",
        "      I_D    = I_Dsat · [ 1 + λ (V_DS − V_Dsat) ]   (channel-length modulation)",
        "",
        "Gate capacitances (Meyer partition):",
        "  Linear / triode:  C_GS = (2/3) C_ox W L,   C_GD = (1/3) C_ox W L",
        "  Saturation:       C_GS = 0.5 × (2/3) C_ox W L,  C_GD ≈ 0",
        "",
        "Drain-bulk depletion capacitance:",
        "  C_DB = Cj0 / (1 + V_DS / V_bi)^m",
    ]
    print("\n".join(eqs))
    print("\n" + "—" * 72 + "\n")


# ────────────────────────────────────────────────────────────────────────────────
# Main script entry point
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # ▸ Load parameters from JSON.  Substitute your own path or dict.
    json_path = "PyShorts/sicmos/sicmos_BSIM3v3.json"
    log_path  = "PyShorts/sicmos/param_log.txt"
    params, meta = load_params_from_json(json_path)

    # ▸ Pretty console header (and logfile) so you can eyeball parameters.
    pretty_header(params, meta, log_path)

    # ▸ Echo equations once so they are visible in the run log.
    print_equations()

    # ▸ Define sweep space (edit as you wish):
    Vgs_values = np.linspace(0.0, 20.0, 9)     # 0 → 20 V (gate)
    Vds_values = np.linspace(0.0, 1200.0, 9)   # 0 → 1.2 kV (drain)
    T_values   = np.arange(300, 451, 25)       # 300 K → 450 K

    # ▸ Run sweep, save CSV, and plot figures.
    sweep_and_plot(Vgs_values, Vds_values, T_values,
                   params,
                   csv_path="PyShorts/sicmos/sweep_results.csv",
                   show=True)

import numpy as np
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console
import pandas as pd

#?-------------------------------------------------------------------------------------
bsim3_params = {
    'Vth0'      : 1.0,            # Threshold voltage at 300K [V]
    'kT'        : 2e-3,           # Vth temp coefficient [V/K]
    'mu0'       : 500e-4,         # Effective mobility at 300K [m^2/Vs]
    'mu_exp'    : 1.5,            # Mobility degradation exponent
    'Cox'       : 3.45e-3,        # Oxide capacitance per unit area [F/m^2]
    'W'         : 100e-6,         # Transistor width [m]
    'L'         : 1e-6,           # Channel length [m]
    'lambda'    : 0.02,           # Channel length modulation [1/V]
    'Cj0'       : 1e-12,          # Zero-bias junction capacitance [F]
    'Vbi'       : 0.7,            # Built-in potential [V]

    "q": 1.6e-19,                 # Charge [C]
    "k": 1.38e-23,                # Boltzmann constant [J/K]

    "eps_sic": 9.7e-13 * 100,    # SiC permittivity [F/m] (converted from F/cm)
    "eps_ox": 3.45e-13 * 100,    # SiO2 permittivity [F/m] (converted from F/cm)

    "tox": 5e-7 * 1e-2,           # Oxide thickness [m] (converted from cm)
    "ni": 1.5e10* 1e-2,                 # Intrinsic carrier concentration [1/cm^3] (still per cm^3)

    "PPW": 1e17,                  # P-well doping [1/cm^3]
    "NJFET": 1e16* 1e6,                # JFET doping [1/m^3]
    "Nsurf": 1e17,                # Surface doping [1/cm^3]

    "XJPW": 1e-5 * 1e-2,          # Junction depth [m] (converted from cm)
    "dpw": 1e-4 * 1e-2,           # P-well separation [m] (converted from cm)

    "mu": 100* 1e-4,                   # Mobility [m^2/Vs]
    "H_by_eff": 1e-3 * 1e-2,      # Effective height [m] (converted from cm)

    "VFB": -1,                   # Flatband voltage [V]
    "Vsurf": 2,                  # Surface transition voltage [V]

    "mjsurf": 0.5,               # Surface grading coefficient
    "mj": 0.5,                   # Bulk grading coefficient

    "Cj0": 1e-12,                # Junction capacitance at 0V [F]
    "Vj": 0.7,                   # Junction potential [V]

    "m": 0.5,                    # CDS grading coefficient
    "C_overlap": 1e-12,          # CGS overlap capacitance [F]
    "lambda": 0.02,              # Channel-length modulation [1/V]
}

param_meta      = {
                'Vth0': {
                    'equation'        : 'Threshold voltage at 300K',
                    'unit'            : 'V',
                    'description'     : 'Threshold voltage of the MOSFET at 300 K',
                    'source'          : 'Device datasheet or experimental extraction'
                },
                'kT': {
                    'equation'        : 'Vth temperature coefficient',
                    'unit'            : 'V/K',
                    'description'     : 'Coefficient for threshold voltage temperature dependence',
                    'source'          : 'Device datasheet or model parameter'
                },
                'mu0': {
                    'equation'        : 'Effective mobility at 300K',
                    'unit'            : 'm^2/V·s',
                    'description'     : 'Carrier mobility in channel at 300 K',
                    'source'          : 'Model parameter from literature or datasheet'
                },
                'mu_exp': {
                    'equation'        : 'Mobility degradation exponent',
                    'unit'            : 'dimensionless',
                    'description'     : 'Exponent modeling mobility dependence on temperature',
                    'source'          : 'Fitted parameter from experiments'
                },
                'Cox': {
                    'equation'        : 'ε_ox / t_ox',
                    'unit'            : 'F/m^2',
                    'description'     : 'Capacitance of gate oxide per unit area',
                    'source'          : 'Calculated from oxide thickness and permittivity'
                },
                'W': {
                    'equation'        : 'Transistor width',
                    'unit'            : 'm',
                    'description'     : 'Channel width of the MOSFET',
                    'source'          : 'Design layout parameter'
                },
                'L': {
                    'equation'        : 'Channel length',
                    'unit'            : 'm',
                    'description'     : 'Channel length of the MOSFET',
                    'source'          : 'Design layout parameter'
                },
                'lambda': {
                    'equation'        : 'Channel length modulation',
                    'unit'            : '1/V',
                    'description'     : 'Coefficient modeling channel length modulation effect',
                    'source'          : 'Extracted from device characteristics'
                },
                'Cj0': {
                    'equation'        : 'Zero-bias junction capacitance',
                    'unit'            : 'F',
                    'description'     : 'Capacitance of reverse-biased junction at zero bias',
                    'source'          : 'Device datasheet or junction modeling'
                },
                'Vbi': {
                    'equation'        : 'Built-in potential',
                    'unit'            : 'V',
                    'description'     : 'Built-in voltage of the PN junction',
                    'source'          : 'Physical constant or device parameter'
                },
                'm': {
                    'equation'        : 'Grading coefficient',
                    'unit'            : 'dimensionless',
                    'description'     : 'Exponent describing junction capacitance voltage dependence',
                    'source'          : 'Device physics or datasheet'
                }
            }
#?-------------------------------------------------------------------------------------

console         = Console(file=open("PyShorts\sicmos\sicmos_BSIM3v3.log", "w", encoding="utf-8"),force_terminal=True,no_color=True)  

def print_header(params, param_meta, log_file_path):
    table = Table(title="MOSFET Parameters", show_lines=True)
    table.add_column("Quantity", no_wrap=True)
    table.add_column("Value")
    table.add_column("Equation")
    table.add_column("Unit")
    table.add_column("Description")
    table.add_column("Source")
    
    for param, meta in param_meta.items():
        value = params.get(param, "N/A")
        if isinstance(value, float):
            if abs(value) < 1e-3 or abs(value) > 1e3:
                value_str = f"{value:.4e}"  
            else:
                value_str = f"{value:.4f}"
        else:
            value_str = str(value)
        table.add_row(
            param,
            value_str,
            meta.get("equation", ""),
            meta.get("unit", ""),
            meta.get("description", ""),
            meta.get("source", ""),
        )
    
    # Create a temporary Console to capture output (no colors)
    temp_console = Console(record=True, color_system=None, force_terminal=True, width=120)
    temp_console.print(table)

    # Get the plain text output
    plain_text = temp_console.export_text()

    # Write plain text to log file
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(plain_text)

def phi_t(T):
    #* Calculate the thermal voltage at temperature T
    #* using the Boltzmann constant and charge
    k = bsim3_params['k']  # Boltzmann constant [J/K]
    q = bsim3_params['q']  # Charge of an electron [C]
    return (k*T)/q

def phi(T):#* Calculate the potential barrier at temperature T
    ni      = bsim3_params['ni']        # Intrinsic carrier concentration
    PPW     = bsim3_params['PPW']       # P-well doping concentration
    NJFET   = bsim3_params['NJFET']     # JFET doping concentration
    return phi_t(T) * np.log(NJFET * PPW / (ni**2))

def alpha():#* Calculate the depletion factor
    eps_sic = bsim3_params['eps_sic']   # Permittivity of SiC
    q       = bsim3_params['q']         # Charge of an electron
    PPW     = bsim3_params['PPW']       # P-well doping concentration
    NJFET   = bsim3_params['NJFET']     # JFET doping concentration
    return np.sqrt((2 * eps_sic * PPW) / (q * NJFET * (NJFET + PPW)))

def VTO_func(T): # * Calculate the threshold voltage at temperature T
    dpw     = bsim3_params['dpw']       # P-well separation
    return float(phi(T) - (dpw / (2 * alpha()))**2)

def rho(): #* Calculate the resistivityas a function of mobility mu
    mu      = bsim3_params['mu']        # Mobility
    q       = bsim3_params['q']         # Charge of an electron
    NJFET   = bsim3_params['NJFET']     # JFET doping concentration 
    return 1 / (q * NJFET * mu)

def beta_func(T):#* Calculate the transconductance parameter
    H_by_eff = bsim3_params['H_by_eff']  # Effective height
    XJPW     = bsim3_params['XJPW']      # Junction depth
    dpw      = bsim3_params['dpw']       # P-well separation
    beta     = ((2 * H_by_eff) / (XJPW * rho() *  (- VTO_func(T))) ) * ((dpw/2)-alpha()*np.sqrt(phi(T)))
    return float(beta) 

def Cox():#* Calculate the oxide capacitance
    eps_ox  = bsim3_params['eps_ox']    # Permittivity of SiO2
    tox     = bsim3_params['tox']       # Oxide thickness
    return eps_ox / tox

def Wdep1_num(VDS_val, VGS_val):#* Calculate the depletion width for the first region
    eps_sic = bsim3_params['eps_sic']   # Permittivity of SiC
    q       = bsim3_params['q']         # Charge of an electron
    Nsurf   = bsim3_params['Nsurf']     # Surface doping concentration
    VFB     = bsim3_params['VFB']       # Flatband voltage
    Vsurf   = bsim3_params['Vsurf']     # Surface transition voltage
    mjsurf  = bsim3_params['mjsurf']    # Surface grading coefficient
    return np.sqrt((2 * eps_sic) / (q * Nsurf) * min(VDS_val - VGS_val - VFB, Vsurf)**mjsurf)

def Wdep2_num(VDS_val, VGS_val, T_val):#* Calculate the depletion width for the second region
    eps_sic = bsim3_params['eps_sic']   # Permittivity of SiC
    q       = bsim3_params['q']         # Charge of an electron
    Nsurf   = bsim3_params['Nsurf']     # Surface doping concentration
    VFB     = bsim3_params['VFB']       # Flatband voltage
    Vsurf   = bsim3_params['Vsurf']     # Surface transition voltage
    mj      = bsim3_params['mj']    # Surface grading coefficient
    return np.sqrt((2 * eps_sic) / (q * Nsurf) * min(VDS_val - VGS_val - VFB - Vsurf, phi(T_val) - VTO_func(T_val))**mj)

def Cdep_num(VDS_val, VGS_val, T_val): #* Calculate the depletion capacitance
    eps_sic = bsim3_params['eps_sic']   # Permittivity of SiC
    return eps_sic / ((Wdep1_num(VDS_val, VGS_val) + Wdep2_num(VDS_val, VGS_val, T_val)))

def CGD_num(VDS_val, VGS_val, T_val):#* Calculate the gate-drain capacitance
    return (Cox() * Cdep_num(VDS_val, VGS_val, T_val)) / (Cox() + Cdep_num(VDS_val, VGS_val, T_val))

def CDS_num(VDS):
    """
    Calculate drain-source capacitance (CDS) as a function of VGS, VDS, and T.
    This junction capacitance depends mainly on VDS reverse bias and temperature.
    """
    CJ = bsim3_params['Cj0']        # Junction capacitance per unit area [F/m²]

    Ld = 1e-6    # Diffusion length or depletion width [m], typically ~1µm
    W = bsim3_params['W']          # Transistor width [m]

    A = W * Ld
                   # Effective area [m²]

    Vbias = max(VDS, 0.01)         # Ensure positive bias for depletion model

    # Basic depletion capacitance model (reverse-biased junction)
    VJ = bsim3_params['Vj']      # Junction potential [V]
    m = bsim3_params['m']        # Grading coefficient
    CDS = CJ * A / ((1 + Vbias / VJ) ** m)

    return CDS

def CGS_num(VGS):
    """
    Calculate gate-source capacitance (CGS) as a function of VGS, VDS, and T.
    In most SiC MOSFET models, CGS is weakly dependent on VDS and mainly varies with VGS and temperature.
    """

    Vgs_eff = max(VGS - bsim3_params['Vth0'], 0)

    W = bsim3_params['W']
    L = bsim3_params['L']
    scale = 1.0 + 0.2 * np.tanh(Vgs_eff / 2.0)  # Smooth transition
    CGS = Cox() * W * L * scale

    return CGS

def mosfet_model(Vgs, Vds, T, params):
    Vth     = params['Vth0'] - params['kT'] * (T - 300)   # Temperature-adjusted threshold
    Vgt     = Vgs - Vth                                   # Gate overdrive
    beta    = beta_func(T)                              # Transconductance factor
    lam     = params['lambda']                            # Channel-length modulation

    if Vgt <= 0:
        # Cutoff region
        Id      = 0.0
        Cgs     = 0.0
        Cgd     = 0.0
    elif Vds < Vgt:
        # Linear (Triode) region
        Id      = beta * (2 * Vgt * Vds) * (1 + lam * Vds)
        Cgs     = CGS_num(Vgs)
        Cgd     = CGD_num(Vds, Vgs, T)
    else:
        # Saturation region
        Id      = beta * Vgt**2 * (1 + lam * Vds)
        Cgs     = CGS_num(Vgs)
        Cgd     = 0.0  # In saturation, Cgd is pinched off

    Cds = CDS_num(Vds)

    return {
        'Id'  : Id,
        'Cgs' : Cgs,
        'Cgd' : Cgd,
        'Cds' : Cds
    }

def plot_results(Vgs_values, Vds_values, T_values, bsim3_params, show=True):
    data = []
    for T in T_values:
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                result = mosfet_model(Vgs, Vds, T, bsim3_params)
                data.append({
                    'T': T,
                    'Vgs': Vgs,
                    'Vds': Vds,
                    'Id': result['Id'],
                    'Cgs': result['Cgs'],
                    'Cgd': result['Cgd'],
                    'Cds': result['Cds']
                })

    # Create time array: 1.0 sec total, 1e-3 sec step
    time_steps = int(1.0 / 1e-3)  # = 1000
    time_array = np.linspace(0, 1.0, time_steps)

    # Repeat or tile time to match the number of data points
    total_data_points = len(data)
    time_column = np.resize(time_array, total_data_points)  # Resizes cyclically

    # Build DataFrame with time as the first column
    df = pd.DataFrame(data)
    df.insert(0, 'time', time_column)

    # Save CSV with new column order
    df.to_csv("PyShorts/sicmos/sicmos_BSIM3v3.csv", index=False)

    # Convert to NumPy for plotting
    data_np = df.to_numpy()
    _, T_arr, Vgs_arr, Vds_arr, Id_arr, Cgs_arr, Cgd_arr, Cds_arr = data_np.T

    # Plotting as before
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('MOSFET Characteristics vs Vgs, Vds, T', fontsize=16)

    # Id vs Vgs for different Vds
    for vds in np.unique(Vds_arr):
        idx = (Vds_arr == vds) & (T_arr == 350)
        axs[0, 0].plot(Vgs_arr[idx], Id_arr[idx], label=f'Vds={vds:.1f}V')
    axs[0, 0].set_title('Id vs Vgs (T=350K)')
    axs[0, 0].set_xlabel('Vgs [V]')
    axs[0, 0].set_ylabel('Id [A]')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Id vs Vds for different Vgs
    for vgs in np.unique(Vgs_arr):
        idx = (Vgs_arr == vgs) & (T_arr == 350)
        axs[0, 1].plot(Vds_arr[idx], Id_arr[idx], label=f'Vgs={vgs:.1f}V')
    axs[0, 1].set_title('Id vs Vds (T=350K)')
    axs[0, 1].set_xlabel('Vds [V]')
    axs[0, 1].set_ylabel('Id [A]')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Cgs, Cgd, Cds vs Vds (at Vgs=2.5V, T=350K)
    idx = (Vgs_arr == 2.5) & (T_arr == 350)
    axs[1, 0].plot(Vds_arr[idx], Cgs_arr[idx], label='Cgs')
    axs[1, 0].plot(Vds_arr[idx], Cgd_arr[idx], label='Cgd')
    axs[1, 0].plot(Vds_arr[idx], Cds_arr[idx], label='Cds')
    axs[1, 0].set_title('Capacitances vs Vds (Vgs=2.5V, T=350K)')
    axs[1, 0].set_xlabel('Vds [V]')
    axs[1, 0].set_ylabel('Capacitance [F]')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Id vs T at Vgs=15V, Vds=600V
    idx = (Vgs_arr == 15) & (Vds_arr == 600)
    axs[1, 1].plot(T_arr[idx], Id_arr[idx])
    axs[1, 1].set_title('Id vs Temperature (Vgs=15V, Vds=600V)')
    axs[1, 1].set_xlabel('Temperature [K]')
    axs[1, 1].set_ylabel('Id [A]')
    axs[1, 1].grid(True)

    plt.tight_layout()
    if show:
        plt.show()

if __name__ == "__main__":

    Vgs_values = np.linspace(0.0, 20.0, 9)     # Gate voltage from 0V to 20V
    Vds_values = np.linspace(0.0, 800.0, 9)    # Drain voltage from 0V to 800V
    T_values   = [300, 325, 350, 375, 400, 425, 450]  # Temperature in Kelvin

    print_header(bsim3_params, param_meta, "PyShorts\sicmos\sicmos_BSIM3v3.log")
    plot_results(Vgs_values, Vds_values, T_values, bsim3_params,show=True)
import numpy as np
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console
import pandas as pd

bsim3_params    = {
        'Vth0'      : 1.0,          #? Threshold voltage at 300K [V]
        'kT'        : 2e-3,         #? Vth temp coefficient [V/K]
        'mu0'       : 500e-4,       #? Effective mobility at 300K [m^2/Vs]
        'mu_exp'    : 1.5,          #? Mobility degradation exponent
        'Cox'       : 3.45e-3,      #? Oxide capacitance per unit area [F/m^2]
        'W'         : 100e-6,       #? Transistor width [m]
        'L'         : 1e-6,         #? Channel length [m]
        'lambda'    : 0.02,         #? Channel length modulation [1/V]
        'Cj0'       : 1e-12,        #? Zero-bias junction capacitance [F]
        'Vbi'       : 0.7,          #? Built-in potential [V]
        'm'         : 0.5           #? Grading coefficient
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

def mosfet_model(Vgs, Vds, T, params):
    # Temperature-adjusted parameters
    Vth         = params['Vth0'] - params['kT'] * (T - 300)
    mu_eff      = params['mu0'] * (300 / T)**params['mu_exp'] 
    Cox         = params['Cox']
    W           = params['W']
    L           = params['L']
    Vgt         = Vgs - Vth
    if Vgt <= 0:
        Id      = 0.0  # Cutoff
        Cgs     = 0.0
        Cgd     = 0.0
    elif Vds < Vgt: # Linear region 
        Id      = mu_eff * Cox * (W / L) * (Vgt * Vds - 0.5 * Vds**2)
        Cgs     = (2 / 3) * Cox * W * L
        Cgd     = (1 / 3) * Cox * W * L
    else: # Saturation region
        Id      = 0.5 * mu_eff * Cox * (W / L) * Vgt**2 * (1 + params['lambda'] * Vds)
        Cgs     = (2 / 3) * Cox * W * L / 2
        Cgd     = 0.0  # Pinched off in saturation
    # Cds (junction-based, reverse-biased)
    Cj0         = params['Cj0']
    Vbi         = params['Vbi']
    m           = params['m']
    Cds         = Cj0 / (1 + max(Vds, 0) / Vbi)**m
    return {'Id'    : Id,'Cgs'   : Cgs,'Cgd'   : Cgd,'Cds'   : Cds}

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
    Vds_values = np.linspace(0.0, 1200.0, 9)    # Drain voltage from 0V to 800V
    T_values   = [300, 325, 350, 375, 400, 425, 450]  # Temperature in Kelvin


    print_header(bsim3_params, param_meta, "PyShorts\sicmos\sicmos_BSIM3v3.log")
    plot_results(Vgs_values, Vds_values, T_values, bsim3_params,show=True)
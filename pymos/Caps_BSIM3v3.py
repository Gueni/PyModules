import numpy as np
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console
import pandas as pd
import json
import os

def load_params_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    params = {key: entry['value'] for key, entry in data.items()}
    meta = {key: {k: v for k, v in entry.items() if k != 'value'} for key, entry in data.items()}
    return params, meta

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

    temp_console = Console(record=True, color_system=None, force_terminal=True, width=120)
    temp_console.print(table)

    plain_text = temp_console.export_text()

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


def plot_results(Vgs_values, Vds_values, T_values, params, show=True):
    data = []
    for T in T_values:
        for Vgs in Vgs_values:
            for Vds in Vds_values:
                result = mosfet_model(Vgs, Vds, T, params)
                data.append({
                    'T': T,
                    'Vgs': Vgs,
                    'Vds': Vds,
                    'Id': result['Id'],
                    'Cgs': result['Cgs'],
                    'Cgd': result['Cgd'],
                    'Cds': result['Cds']
                })

    time_steps = int(1.0 / 1e-3)
    time_array = np.linspace(0, 1.0, time_steps)
    total_data_points = len(data)
    time_column = np.resize(time_array, total_data_points)

    df = pd.DataFrame(data)
    df.insert(0, 'time', time_column)
    os.makedirs("PyShorts/sicmos", exist_ok=True)
    df.to_csv("PyShorts/sicmos/sicmos_BSIM3v3.csv", index=False)

    data_np = df.to_numpy()
    _, T_arr, Vgs_arr, Vds_arr, Id_arr, Cgs_arr, Cgd_arr, Cds_arr = data_np.T

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('MOSFET Characteristics vs Vgs, Vds, T', fontsize=16)

    for vds in np.unique(Vds_arr):
        idx = (Vds_arr == vds) & (T_arr == 350)
        axs[0, 0].plot(Vgs_arr[idx], Id_arr[idx], label=f'Vds={vds:.1f}V')
    axs[0, 0].set_title('Id vs Vgs (T=350K)')
    axs[0, 0].set_xlabel('Vgs [V]')
    axs[0, 0].set_ylabel('Id [A]')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    for vgs in np.unique(Vgs_arr):
        idx = (Vgs_arr == vgs) & (T_arr == 350)
        axs[0, 1].plot(Vds_arr[idx], Id_arr[idx], label=f'Vgs={vgs:.1f}V')
    axs[0, 1].set_title('Id vs Vds (T=350K)')
    axs[0, 1].set_xlabel('Vds [V]')
    axs[0, 1].set_ylabel('Id [A]')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    idx = (Vgs_arr == 2.5) & (T_arr == 350)
    axs[1, 0].plot(Vds_arr[idx], Cgs_arr[idx], label='Cgs')
    axs[1, 0].plot(Vds_arr[idx], Cgd_arr[idx], label='Cgd')
    axs[1, 0].plot(Vds_arr[idx], Cds_arr[idx], label='Cds')
    axs[1, 0].set_title('Capacitances vs Vds (Vgs=2.5V, T=350K)')
    axs[1, 0].set_xlabel('Vds [V]')
    axs[1, 0].set_ylabel('Capacitance [F]')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

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
    json_path = "PyShorts/sicmos/sicmos_BSIM3v3.json"
    log_path  = "PyShorts/sicmos/sicmos_BSIM3v3.log"

    params, param_meta = load_params_from_json(json_path)
    print_header(params, param_meta, log_path)
    Vgs_values = np.linspace(0.0, 20.0, 9)
    Vds_values = np.linspace(0.0, 1200.0, 9)
    T_values   = [300, 325, 350, 375, 400, 425, 450]

    plot_results(Vgs_values, Vds_values, T_values, params, show=True)

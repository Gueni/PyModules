import numpy as np
import matplotlib.pyplot as plt
from rich.table import Table
from rich.console import Console
from rich.theme import Theme
from sympy import symbols, Eq, Piecewise, Max, simplify, pprint
from rich.console import Console
from sympy import symbols, Eq, Piecewise, Max, simplify, pretty
from rich.console import Console

# Create a Console that logs to file
from sympy import symbols, Piecewise, Max, simplify, pretty
from rich.console import Console
from rich.panel import Panel
from sympy import symbols, Piecewise, Max, pretty
from rich.console import Console
from rich.table import Table

from sympy import symbols, Piecewise, Max, pretty
from rich.console import Console
from rich.table import Table

# Create a Console that writes to a log file
log_file_path = "PyShorts/DATA/log.log"
console = Console(file=open(log_file_path, "w", encoding="utf-8"), force_terminal=True)

# Define symbols
Vgs, Vds, T = symbols("Vgs Vds T")
Vth0, kT, mu0, mu_exp = symbols("Vth0 kT mu0 mu_exp")
Cox, W, L, lambd = symbols("Cox W L lambda")
Cj0, Vbi, m = symbols("Cj0 Vbi m")

# Derived quantities
Vth = Vth0 - kT * (T - 300)
mu_eff = mu0 * (300 / T)**mu_exp
Vgt = Vgs - Vth

# Define expressions
Id_expr = Piecewise(
    (0, Vgt <= 0),
    (mu_eff * Cox * (W / L) * (Vgt * Vds - 0.5 * Vds**2), Vds < Vgt),
    (0.5 * mu_eff * Cox * (W / L) * Vgt**2 * (1 + lambd * Vds), True)
)

Cgs_expr = Piecewise(
    (0, Vgt <= 0),
    ((2 / 3) * Cox * W * L, Vds < Vgt),
    ((1 / 3) * Cox * W * L, True)
)

Cgd_expr = Piecewise(
    (0, Vgt <= 0),
    ((1 / 3) * Cox * W * L, Vds < Vgt),
    (0, True)
)

Cds_expr = Cj0 / (1 + Max(Vds, 0) / Vbi)**m

# Prepare the table
table = Table(title="Symbolic MOSFET Model Equations")

table.add_column("Equation", style="cyan", no_wrap=True)
table.add_column("Expression", style="magenta")

table.add_row("Id (Drain Current)", pretty(Id_expr, use_unicode=True))
table.add_row("Cgs (Gate-Source Capacitance)", pretty(Cgs_expr, use_unicode=True))
table.add_row("Cgd (Gate-Drain Capacitance)", pretty(Cgd_expr, use_unicode=True))
table.add_row("Cds (Drain-Source Capacitance)", pretty(Cds_expr, use_unicode=True))
console = Console(file=open(log_file_path, "w", encoding="utf-8"), force_terminal=True, color_system=None)

# Print the table to the log file
console.print(table)







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

    return {
        'Id'    : Id,
        'Cgs'   : Cgs,
        'Cgd'   : Cgd,
        'Cds'   : Cds
    }

if __name__ == "__main__":

    bsim3_params = {
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

custom_theme    = Theme({"log": "green"})
console         = Console(file=open("PyShorts\DATA\log.log", "a", encoding="utf-8"), theme=custom_theme)
Vgs_values      = np.linspace(0.0, 3.0, 7)     
Vds_values      = np.linspace(0.0, 3.0, 7)     
T_values        = [300, 325, 350, 375, 400]   

for T in T_values:
    table = Table(title=f"MOSFET Sweep Results @ T = {T} K", show_lines=True)
    table.add_column("Vgs [V]", justify="right")
    table.add_column("Vds [V]", justify="right")
    table.add_column("Id [A]", justify="right")
    table.add_column("Cgs [F]", justify="right")
    table.add_column("Cgd [F]", justify="right")
    table.add_column("Cds [F]", justify="right")

    for Vgs in Vgs_values:
        for Vds in Vds_values:
            result = mosfet_model(Vgs, Vds, T, bsim3_params)
            table.add_row(
                f"{Vgs:.2f}",
                f"{Vds:.2f}",
                f"{result['Id']:.4e}",
                f"{result['Cgs']:.4e}",
                f"{result['Cgd']:.4e}",
                f"{result['Cds']:.4e}"
            )

    console.print(table)

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

data_np = np.array([
    (d['T'], d['Vgs'], d['Vds'], d['Id'], d['Cgs'], d['Cgd'], d['Cds'])
    for d in data
])
T_arr, Vgs_arr, Vds_arr, Id_arr, Cgs_arr, Cgd_arr, Cds_arr = data_np.T
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('MOSFET Characteristics vs Vgs, Vds, T', fontsize=16)
# Id vs Vgs for different Vds
for vds in np.unique(Vds_arr):
    idx = (Vds_arr == vds) & (T_arr == 350)  # fixed T
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

# Optional: Id vs T at Vgs=2.5V, Vds=2.0V
idx = (Vgs_arr == 2.5) & (Vds_arr == 2.0)
axs[1, 1].plot(T_arr[idx], Id_arr[idx])
axs[1, 1].set_title('Id vs Temperature (Vgs=2.5V, Vds=2.0V)')
axs[1, 1].set_xlabel('Temperature [K]')
axs[1, 1].set_ylabel('Id [A]')
axs[1, 1].grid(True)

plt.tight_layout()
plt.show()
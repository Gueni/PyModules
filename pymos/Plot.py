
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
#? Name:        Plot.py
#? Purpose:     Plot simulation outputs such as I-V and C-V curves
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import pandas as pd
import matplotlib.pyplot as plt
import os
#? -------------------------------------------------------------------------------
class MOSFETPlotter:
    def __init__(self, csv_path):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Data file not found at {csv_path}")
        self.df = pd.read_csv(csv_path)
        self._validate_columns()

    def _validate_columns(self):
        required_cols = {"time", "VGS", "VDS", "ID", "CGS", "CGD", "CDS", "T"}
        if not required_cols.issubset(self.df.columns):
            raise ValueError(f"CSV must contain the following columns: {required_cols}")

    def plot(self, show=True):
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("MOSFET Simulation Results", fontsize=16)

        self._plot_id_vs_vgs(axs[0, 0])
        self._plot_id_vs_vds(axs[0, 1])
        self._plot_id_vs_temp(axs[1, 0])
        self._plot_caps_vs_vds(axs[1, 1])

        if show:
            plt.show()

    def _plot_id_vs_vgs(self, ax):
        ax.plot(self.df["VGS"], self.df["ID"], label="ID vs VGS", color='blue')
        ax.set_xlabel("VGS (V)")
        ax.set_ylabel("ID (A)")
        ax.set_title("ID vs VGS")
        ax.grid(True)
        ax.legend()

    def _plot_id_vs_vds(self, ax):
        ax.plot(self.df["VDS"], self.df["ID"], label="ID vs VDS", color='green')
        ax.set_xlabel("VDS (V)")
        ax.set_ylabel("ID (A)")
        ax.set_title("ID vs VDS")
        ax.grid(True)
        ax.legend()

    def _plot_id_vs_temp(self, ax):
        ax.plot(self.df["T"], self.df["ID"], label="ID vs Temperature", color='black')
        ax.set_xlabel("T (K)")
        ax.set_ylabel("ID (A)")
        ax.set_title("ID vs Temperature")
        ax.grid(True)
        ax.legend()

    def _plot_caps_vs_vds(self, ax):
        ax.plot(self.df["T"], self.df["CGS"], label="CGS", color='red')
        ax.plot(self.df["T"], self.df["CGD"], label="CGD", color='orange')
        ax.plot(self.df["T"], self.df["CDS"], label="CDS", color='purple')
        ax.set_xlabel('Vds [V]')
        ax.set_ylabel("Capacitance (F)")
        ax.set_title('Capacitances vs Vds (Vgs=2.5V, T=300K)')
        ax.grid(True)
        ax.legend()

#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    csv_path = r'D:\WORKSPACE\Python_code\pymos\data\shichman_hodges.csv'
    plotter = MOSFETPlotter(csv_path)
    plotter.plot()
#? -------------------------------------------------------------------------------
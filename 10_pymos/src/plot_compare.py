
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
#? Name:        plot_compare.py
#? Purpose:     Plot and compare simulation results from different MOSFET models
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#? -------------------------------------------------------------------------------
class MOSFETModelComparer:
    def __init__(self, csv1_path, csv2_path):
        self.df1 = pd.read_csv(csv1_path)
        self.df2 = pd.read_csv(csv2_path)
        self._validate_columns()
        self._unpack_data()

    def _validate_columns(self):
        required_cols = {"time", "T", "VGS", "VDS", "ID", "CGS", "CGD", "CDS"}
        if not required_cols.issubset(self.df1.columns) or not required_cols.issubset(self.df2.columns):
            raise ValueError(f"Both CSVs must contain the following columns: {required_cols}")

    def _unpack_data(self):
        arr1 = self.df1.to_numpy()
        arr2 = self.df2.to_numpy()
        _, self.T1, self.Vgs1, self.Vds1, self.Id1, self.Cgs1, self.Cgd1, self.Cds1 = arr1.T
        _, self.T2, self.Vgs2, self.Vds2, self.Id2, self.Cgs2, self.Cgd2, self.Cds2 = arr2.T

    def plot(self, show=True):
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Comparison of Two MOSFET Models', fontsize=16)

        self._plot_id_vs_vgs(axs[0, 0])
        self._plot_id_vs_vds(axs[0, 1])
        self._plot_caps_vs_vds(axs[1, 0])
        self._plot_id_vs_temp(axs[1, 1])

        if show:
            plt.show()

    def _plot_id_vs_vgs(self, ax):
        for vds in np.unique(self.Vds1):
            idx1 = (self.Vds1 == vds) & (self.T1 == 300)
            idx2 = (self.Vds2 == vds) & (self.T2 == 300)
            if np.any(idx1):
                ax.plot(self.Vgs1[idx1], self.Id1[idx1], label=f'Model 1 Vds={vds:.1f}V', linestyle='-')
            if np.any(idx2):
                ax.plot(self.Vgs2[idx2], self.Id2[idx2], label=f'Model 2 Vds={vds:.1f}V', linestyle='--')
        ax.set_title('Id vs Vgs (T=300K)')
        ax.set_xlabel('Vgs [V]')
        ax.set_ylabel('Id [A]')
        ax.legend()
        ax.grid(True)

    def _plot_id_vs_vds(self, ax):
        for vgs in np.unique(self.Vgs1):
            idx1 = (self.Vgs1 == vgs) & (self.T1 == 300)
            idx2 = (self.Vgs2 == vgs) & (self.T2 == 300)
            if np.any(idx1):
                ax.plot(self.Vds1[idx1], self.Id1[idx1], label=f'Model 1 Vgs={vgs:.1f}V', linestyle='-')
            if np.any(idx2):
                ax.plot(self.Vds2[idx2], self.Id2[idx2], label=f'Model 2 Vgs={vgs:.1f}V', linestyle='--')
        ax.set_title('Id vs Vds (T=300K)')
        ax.set_xlabel('Vds [V]')
        ax.set_ylabel('Id [A]')
        ax.legend()
        ax.grid(True)

    def _plot_caps_vs_vds(self, ax):
        idx1 = (self.Vgs1 == 2.5) & (self.T1 == 300)
        idx2 = (self.Vgs2 == 2.5) & (self.T2 == 300)
        ax.plot(self.Vds1[idx1], self.Cgs1[idx1], label='Model 1 Cgs', linestyle='-')
        ax.plot(self.Vds1[idx1], self.Cgd1[idx1], label='Model 1 Cgd', linestyle='-')
        ax.plot(self.Vds1[idx1], self.Cds1[idx1], label='Model 1 Cds', linestyle='-')
        ax.plot(self.Vds2[idx2], self.Cgs2[idx2], label='Model 2 Cgs', linestyle='--')
        ax.plot(self.Vds2[idx2], self.Cgd2[idx2], label='Model 2 Cgd', linestyle='--')
        ax.plot(self.Vds2[idx2], self.Cds2[idx2], label='Model 2 Cds', linestyle='--')
        ax.set_title('Capacitances vs Vds (Vgs=2.5V, T=300K)')
        ax.set_xlabel('Vds [V]')
        ax.set_ylabel('Capacitance [F]')
        ax.legend()
        ax.grid(True)

    def _plot_id_vs_temp(self, ax):
        idx1 = (self.Vgs1 == 15) & (self.Vds1 == 600)
        idx2 = (self.Vgs2 == 15) & (self.Vds2 == 600)
        ax.plot(self.T1[idx1], self.Id1[idx1], label='Model 1', linestyle='-')
        ax.plot(self.T2[idx2], self.Id2[idx2], label='Model 2', linestyle='--')
        ax.set_title('Id vs Temperature (Vgs=15V, Vds=600V)')
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Id [A]')
        ax.legend()
        ax.grid(True)
#? -------------------------------------------------------------------------------

if __name__ == "__main__":
    csv1 = r'D:\WORKSPACE\PyModules\10_pymos\data\shichman_hodges.csv'
    csv2 = r'D:\WORKSPACE\PyModules\10_pymos\data\BSIM3v3.csv'
    comparer = MOSFETModelComparer(csv1, csv2)
    comparer.plot()
#? -------------------------------------------------------------------------------
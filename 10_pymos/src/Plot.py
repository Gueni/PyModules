
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
#? Name:        plot.py
#? Purpose:     Plot and compare results from different MOSFET models using Plotly
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#?
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import os
#? -------------------------------------------------------------------------------

class MOSFETModelComparer:
    def __init__(self, csv1_path, csv2_path, output_html=None):
        self.df1 = pd.read_csv(csv1_path)
        self.df2 = pd.read_csv(csv2_path)
        self.output_html = output_html or r'D:\WORKSPACE\PyModules\10_pymos\data\comparison_plot.html'
        self._validate_columns()
        self._unpack_data()

    def _validate_columns(self):
        required_cols = {"time", "T", "VGS", "VDS", "ID", "CGS", "CGD", "CDS"}
        if not required_cols.issubset(self.df1.columns) or not required_cols.issubset(self.df2.columns):
            raise ValueError(f"Both CSVs must contain the following columns: {required_cols}")

    def _unpack_data(self):
        self.time1, self.time2 = self.df1["time"], self.df2["time"]
        self.T1, self.T2 = self.df1["T"], self.df2["T"]
        self.Vgs1, self.Vgs2 = self.df1["VGS"], self.df2["VGS"]
        self.Vds1, self.Vds2 = self.df1["VDS"], self.df2["VDS"]
        self.Id1, self.Id2 = self.df1["ID"], self.df2["ID"]
        self.Cgs1, self.Cgs2 = self.df1["CGS"], self.df2["CGS"]
        self.Cgd1, self.Cgd2 = self.df1["CGD"], self.df2["CGD"]
        self.Cds1, self.Cds2 = self.df1["CDS"], self.df2["CDS"]

    def plot(self):
        figures = []

        # --- Id vs Time ---
        fig_id_time = go.Figure()
        fig_id_time.add_trace(go.Scatter(x=self.time1, y=self.Id1, name="BSIM Id", line=dict(dash='solid')))
        fig_id_time.add_trace(go.Scatter(x=self.time2, y=self.Id2, name="SH Id", line=dict(dash='dot')))
        fig_id_time.update_layout(title="Id vs Time", xaxis_title="Time", yaxis_title="Id [A]", legend=dict(x=1, y=1))
        figures.append(fig_id_time)

        # --- Capacitances vs Time ---
        fig_caps_time = go.Figure()
        for name, c1, c2 in [("Cgs", self.Cgs1, self.Cgs2), ("Cgd", self.Cgd1, self.Cgd2), ("Cds", self.Cds1, self.Cds2)]:
            fig_caps_time.add_trace(go.Scatter(x=self.time1, y=c1, name=f"BSIM {name}", line=dict(dash='solid')))
            fig_caps_time.add_trace(go.Scatter(x=self.time2, y=c2, name=f"SH {name}", line=dict(dash='dot')))
        fig_caps_time.update_layout(title="Capacitances vs Time", xaxis_title="Time", yaxis_title="Capacitance [F]", legend=dict(x=1, y=1))
        figures.append(fig_caps_time)

        # --- Capacitances vs Vds ---
        fig_caps_vds = go.Figure()
        for name, c1, c2 in [("Cgs", self.Cgs1, self.Cgs2), ("Cgd", self.Cgd1, self.Cgd2), ("Cds", self.Cds1, self.Cds2)]:
            fig_caps_vds.add_trace(go.Scatter(x=self.Vds1, y=c1, name=f"BSIM {name}", line=dict(dash='solid')))
            fig_caps_vds.add_trace(go.Scatter(x=self.Vds2, y=c2, name=f"SH {name}", line=dict(dash='dot')))
        fig_caps_vds.update_layout(title="Capacitances vs Vds", xaxis_title="Vds [V]", yaxis_title="Capacitance [F]", legend=dict(x=1, y=1))
        figures.append(fig_caps_vds)

        # --- Capacitances vs Vgs ---
        fig_caps_vgs = go.Figure()
        for name, c1, c2 in [("Cgs", self.Cgs1, self.Cgs2), ("Cgd", self.Cgd1, self.Cgd2), ("Cds", self.Cds1, self.Cds2)]:
            fig_caps_vgs.add_trace(go.Scatter(x=self.Vgs1, y=c1, name=f"BSIM {name}", line=dict(dash='solid')))
            fig_caps_vgs.add_trace(go.Scatter(x=self.Vgs2, y=c2, name=f"SH {name}", line=dict(dash='dot')))
        fig_caps_vgs.update_layout(title="Capacitances vs Vgs", xaxis_title="Vgs [V]", yaxis_title="Capacitance [F]", legend=dict(x=1, y=1))
        figures.append(fig_caps_vgs)

        # --- Id vs Temperature ---
        fig_id_temp = go.Figure()
        idx1 = (self.Vgs1 == 15) & (self.Vds1 == 600)
        idx2 = (self.Vgs2 == 15) & (self.Vds2 == 600)
        fig_id_temp.add_trace(go.Scatter(x=self.T1[idx1], y=self.Id1[idx1], name="BSIM Id", line=dict(dash='solid')))
        fig_id_temp.add_trace(go.Scatter(x=self.T2[idx2], y=self.Id2[idx2], name="SH Id", line=dict(dash='dot')))
        fig_id_temp.update_layout(title="Id vs Temperature (Vgs=15V, Vds=600V)", xaxis_title="Temperature [K]", yaxis_title="Id [A]", legend=dict(x=1, y=1))
        figures.append(fig_id_temp)

        # --- Id vs Vgs ---
        fig_id_vgs = go.Figure()
        for vds in np.unique(self.Vds1):
            i1 = (self.Vds1 == vds) & (self.T1 == 300)
            i2 = (self.Vds2 == vds) & (self.T2 == 300)
            if np.any(i1):
                fig_id_vgs.add_trace(go.Scatter(x=self.Vgs1[i1], y=self.Id1[i1], name=f"BSIM Vds={vds:.1f}", line=dict(dash='solid')))
            if np.any(i2):
                fig_id_vgs.add_trace(go.Scatter(x=self.Vgs2[i2], y=self.Id2[i2], name=f"SH Vds={vds:.1f}", line=dict(dash='dot')))
        fig_id_vgs.update_layout(title="Id vs Vgs (T=300K)", xaxis_title="Vgs [V]", yaxis_title="Id [A]", legend=dict(x=1, y=1))
        figures.append(fig_id_vgs)

        # --- Id vs Vds ---
        fig_id_vds = go.Figure()
        for vgs in np.unique(self.Vgs1):
            i1 = (self.Vgs1 == vgs) & (self.T1 == 300)
            i2 = (self.Vgs2 == vgs) & (self.T2 == 300)
            if np.any(i1):
                fig_id_vds.add_trace(go.Scatter(x=self.Vds1[i1], y=self.Id1[i1], name=f"BSIM Vgs={vgs:.1f}", line=dict(dash='solid')))
            if np.any(i2):
                fig_id_vds.add_trace(go.Scatter(x=self.Vds2[i2], y=self.Id2[i2], name=f"SH Vgs={vgs:.1f}", line=dict(dash='dot')))
        fig_id_vds.update_layout(title="Id vs Vds (T=300K)", xaxis_title="Vds [V]", yaxis_title="Id [A]", legend=dict(x=1, y=1))
        figures.append(fig_id_vds)

        # --- Export all figures to one HTML ---
        os.makedirs(os.path.dirname(self.output_html), exist_ok=True)
        html_parts = [pio.to_html(fig, full_html=False, include_plotlyjs='cdn') for fig in figures]
        full_html = "<html><head><title>MOSFET Comparison</title></head><body>\n" + "\n<hr>\n".join(html_parts) + "\n</body></html>"

        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(full_html)

        print(f"HTML with all plots saved to: {self.output_html}")
#? -------------------------------------------------------------------------------

if __name__ == "__main__":
    csv1 = r'D:\WORKSPACE\PyModules\10_pymos\data\shichman_hodges.csv'
    csv2 = r'D:\WORKSPACE\PyModules\10_pymos\data\BSIM3v3.csv'
    comparer = MOSFETModelComparer(csv1, csv2)
    comparer.plot()
#? -------------------------------------------------------------------------------

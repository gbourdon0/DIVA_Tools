import os

import numpy as np

from modules.data_reader.Tecplot import Tecplot

from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import matplotlib.pyplot as plt
from modules.data_reader.pickle_reader import PickleReader as pr
import modules.diva_input as DIVA_in
from scipy import constants
import modules.diva_input as DIVA

diva_input = DIVA.diva_input()
import pandas as pd

paf = "/home/gbourdon/03_DIVA_dev/000_BENCHMARK/05_conv_nat_benchmark"
configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/images")
filename = "wall_018.pickle"
diva_input.load(paf + "/run")
wall = pr()
wall.load_file(paf + "/post_traitement/data1D/wall/" + filename)
print(wall.get_header())
print(wall.key_list)
###### PARAM TEST
R = diva_input.IC.solid_obj_dim[0]
D = 2 * R
nu_gas = diva_input.PP.mu_vap / diva_input.PP.rho_vap
alpha_gas = diva_input.TP.kth_vap / (diva_input.PP.rho_vap * diva_input.TP.cp_vap)
beta = 1 / diva_input.IC.Tp_inf

##### Get heatflux from article
bench = pd.read_csv("article_ra1e5.txt", sep=';')
bench["Nu"] = bench["Nu/Ra**.25"] * (1e5 ** .25)
bench["h_ws"] = bench["Nu"] * diva_input.TP.kth_vap / D
bench["heat_flux"] = bench["h_ws"] * 32.5  # 32.5  = DT
avg = np.average(bench["heat_flux"])
print(f" Average heat flux from article is {avg:.{4}}")
##### ADIMENSIONNAL NUMBER
Gr = constants.g * D ** 3 * (diva_input.IC.T_immersed - diva_input.IC.Tp_inf) * beta * diva_input.PP.rho_vap ** 2 / (
        diva_input.PP.mu_vap ** 2)
Pr = diva_input.PP.mu_vap * diva_input.TP.cp_vap / diva_input.TP.kth_vap
Ra = constants.g * D ** 3 * (diva_input.IC.T_immersed - diva_input.IC.Tp_inf) * beta / (
        nu_gas * alpha_gas)

print(Ra**.25/D)
h = -wall[filename]["FLUX_wall"] / (diva_input.IC.T_immersed - diva_input.IC.Tp_inf)
Nu = h * D / diva_input.TP.kth_vap
##### Plot
# plt.plot(wall["wall_015.pickle"]["theta_wall"], -wall["wall_015.pickle"]["h_ws"] )
plt.scatter(bench["Angle"], bench["Nu"], label="Ra = 1e5, Paper")
plt.scatter(wall[filename]["theta_wall"], Nu, label=f"Ra = {Ra:.{2}}, DIVA")
plt.xlabel(r"$\theta$ (deg)")
plt.ylabel("Heat flux (W/m$^2$)")
plt.legend()
plt.show()

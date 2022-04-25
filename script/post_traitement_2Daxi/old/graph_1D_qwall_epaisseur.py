from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import seaborn as sns

import pandas as pd
import modules.diva_input as DIVA_in



paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
#paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
configure_latex(style="seaborn-bright", global_save_path=paf + "/post_traitement/images")
bbox = dict(boxstyle="round", fc="1")

# load data
DIVA_input = DIVA_in.diva_input()
DIVA_input.load(paf+"/run")
time = pd.read_csv(paf + "post_traitement/time.csv", sep=";")
time = np.array(time["time (s)"])
wall = pr()
wall.load_folder(paf + "post_traitement/data1D/wall")
wall.define_time(time)  # Associated a time list with the data
print(wall.get_header())

interface = pr()
interface.load_folder(paf + "post_traitement/data1D/interface")
interface.define_time(time)  # Associated a time list with the data
print(interface.get_header())

from scipy.interpolate import interp1d

theta_max = 170
theta = np.arange(2, theta_max, 1)
df = wall[wall.key_list[-1]].loc[wall[wall.key_list[-1]]["theta_wall"] < theta_max]

flux = interp1d(df["theta_wall"], -df["FLUX_wall"],
                kind='cubic', fill_value="extrapolate")
df = interface[interface.key_list[-1]].loc[interface[interface.key_list[-1]]["theta_interface"] < theta_max]
thickness = interp1d(df["theta_interface"], 1000 * df["Film thickness"],
                     kind='cubic', fill_value="extrapolate")

flux_plot = flux(theta)
thickness_plot = thickness(theta)
cond_flux = DIVA_input.TP.kth_vap * (DIVA_input.IC.T_immersed - DIVA_input.TP.t_sat) / thickness_plot * 1000

fig, (ax1, ax2) = plt.subplots(1, 2)
set_size(subplots=(1, 2))
ax1_bis = ax1.twiny()

ax1.plot(thickness_plot, flux_plot, label='DIVA computed heat flux')
ax1.plot(thickness_plot, cond_flux, label="Conduction flux")
ax1.grid(visible=True)
ax1.set_ylabel(r"Wall heat flux (W/m$^2$)")
ax1.set_xlabel(r"Film thickness (mm)")
ax1.legend()

ax1_bis.set_xlim(ax1.get_xlim())
theta_plot = [0,150,160,165,169,theta_max]
ax1_bis.set_xticks(thickness(theta_plot))
tick = [str(elem) for elem in theta_plot]
ax1_bis.set_xlabel(r"$\Theta$ (deg)")
ax1_bis.set_xticklabels(tick)

theta_zoom = 110
ax2.plot(thickness_plot[0:theta_zoom], flux_plot[0:theta_zoom], label='DIVA computed heat flux')
ax2.plot(thickness_plot[0:theta_zoom], cond_flux[0:theta_zoom], label="Conduction flux")
ax2.grid(visible=True)
ax2.set_ylabel(r"Wall heat flux (W/m$^2$)")
ax2.set_xlabel(r"Film thickness (mm)")
ax2.legend()

ax2_bis = ax2.twiny()
ax2_bis.set_xlim(ax2.get_xlim())
theta_plot = [0,50,60,70,80,theta_zoom]
ax2_bis.set_xticks(thickness(theta_plot))
tick = [str(elem) for elem in theta_plot]
ax2_bis.set_xlabel(r"$\Theta$ (deg)")
ax2_bis.set_xticklabels(tick)
savefig("Qwall_thickness", pickle = fig, format="png", dpi=1000)
plt.show()

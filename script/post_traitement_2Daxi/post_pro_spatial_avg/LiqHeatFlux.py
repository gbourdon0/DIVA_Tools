from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import pandas as pd
import modules.diva_input as DIVA_in

########################################################################################################################
#                                       Loading data
########################################################################################################################
# Input
paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
#paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/images")
DEBUG = True
# load data
DIVA_input = DIVA_in.diva_input()
DIVA_input.load(paf + "/run")
time = pd.read_csv(paf + "post_traitement/time.csv", sep=";")
time = np.array(time["time (s)"])
wall = pr()
wall.load_folder(paf + "post_traitement/data1D/interface")
wall.define_time(time)  # Associated a time list with the data
print(wall[wall.key_list[0]].columns)

'''plt.plot(wall[wall.key_list[150]]["theta_interface"],wall[wall.key_list[150]]["FLUX_liq"])
plt.show()'''
out = []
from scipy.integrate import trapz
for key in wall.key_list:
    df = wall[key]
    X,Y = np.array( df["theta_interface"]), np.array(df["FLUX_evap"])
    X,Y = X[::-1],Y[::-1]
    integral = np.trapz(Y,X)/(X[-1]-X[0])
    out.append(integral)

plt.plot(time,out)

plt.show()

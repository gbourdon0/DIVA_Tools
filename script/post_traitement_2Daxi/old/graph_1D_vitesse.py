from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import modules.post_proc_2D as pt
import seaborn as sns
import modules.analytique_solutions.sphere as sp
import pandas as pd
import modules.diva_input as DIVA_in

paf = "/home/gbourdon/02_DIVA_benchmark_drag/11_5d-1/"
configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/images")
bbox = dict(boxstyle="round", fc="1")

# load data
'''time = pd.read_csv(paf + "post_traitement/time.csv", sep=";")
time = np.array(time["time (s)"])'''
data_1D = pr()
data_1D.load_file(paf+"post_traitement/data2D/200.pickle")
#data_1D.load_folder(paf+"post_traitement/data1D/interface")
##data_1D.define_time(time)  # Associated a time list with the data
print(data_1D.get_header())

DIVA_input = DIVA_in.diva_input()
DIVA_input.load(paf +"/run")

df =data_1D["200.pickle"]
#df['Theta_polar'] = np.rad2deg(df['Theta_polar']+np.pi/2)
df1 = df.loc[(df["R_polar"] <= 0.04) & (df["Theta_polar"] > 42) & (df["Theta_polar"] < 44)]
step = abs(df["R"][0] - df["R"][1])
def plot():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    extent = [df["R"].min(), df["R"].max(), df["Z"].min(), df["Z"].max()]
    toplot = np.array(df["Theta_polar"]).reshape(1024, 512)
    img = ax.imshow(toplot, extent=extent, origin="lower")
    cb = fig.colorbar(img)
    cb.set_label("temperature")

    plt.scatter(df1["R"],df1["Z"])
    from modules.global_variable.param import plot_param

    plt.show()
theta_plot = [45]
for angle in theta_plot:
    r = np.arange(0, 0.04, 0.0001)
    theta = np.array([angle] * len(r))
    df_liq = df.loc[(df["Theta_polar"] > angle-1) & (df["Theta_polar"] < angle +1) & (df["Phi_solid"]<0) & (df["Phi"]>0)]
    df_gas = df.loc[(df["Theta_polar"] > angle-1) & (df["Theta_polar"] < angle +1) & (df["Phi_solid"]<0) & (df["Phi"]<0)]
    df1 = df.loc[(df["Theta_polar"] > angle-1) & (df["Theta_polar"] < angle +1) & (df["Phi_solid"]<0)]

    nearest = pt.interp2D(np.array(df1["U_polar_theta"]), np.array(df1["R_polar"]), np.array(df1["Theta_polar"]), r, theta,
                       resolve_nan=True, kind="nearest")  # to find the minimum value which is zero
    liq_val = pt.interp2D(np.array(df_liq["U_polar_theta"]), np.array(df_liq["R_polar"]), np.array(df_liq["Theta_polar"]), r, theta,
                       resolve_nan=True, kind="linear")  # to find the minimum value which is zero
    gas_val = pt.interp2D(np.array(df_gas["U_polar_theta"]), np.array(df_gas["R_polar"]),
                          np.array(df_gas["Theta_polar"]), r, theta,
                          resolve_nan=True, kind="linear")  # to find the minimum value which is zero
    phi = pt.interp2D(np.array(df1["Phi"]), np.array(df1["R_polar"]), np.array(df1["Theta_polar"]), r, theta,
                       resolve_nan=True, kind="linear")  # to find the minimum value which is zero
    val = []
    for gas,liq,phi1 in zip(gas_val,liq_val,phi):
        if phi1>0:
            val.append(liq)
        else:
            val.append(gas)
    dif = np.absolute(df1["Phi"] - 0)
    change = np.array(df1["R_polar"])[dif.argmin()]
    plt.vlines(0.005,min(nearest),max(nearest), label ="wall", color = "k")
    plt.vlines(change,min(nearest),max(nearest), label ="Interface", color = "k")
    plt.plot(r, nearest, label = "nearest")
    plt.plot(r, val, label="Linear")
plt.legend()
plt.show()

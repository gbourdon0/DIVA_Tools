from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import seaborn as sns

import pandas as pd


# INPUT

'''paf = "/home/gbourdon/02_DIVA_benchmark_drag/11_5d-1/post_traitement"
configure_latex(style="seaborn-bright", global_save_path=paf + "/images")
bbox = dict(boxstyle="round", fc="1")

# Load data
time = pd.read_csv(paf + "/time.csv", sep=";")
time = np.array(time["time (s)"])
data_1D = pr()
data_1D.load_folder("/home/gbourdon/02_DIVA_benchmark_drag/11_5d-1/post_traitement/data1D/wall")
data_1D.define_time(time)
print(data_1D.get_header())'''

# Plot
def wall_heat_flux(data_1D, time):
    bbox = dict(boxstyle="round", fc="1")
    # ***************************** Wall heat flux
    plt_min = data_1D.time2plt(time)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    set_size(subplots=(1, 2))
    convergence = []  # check convergence
    mean = np.zeros(len(data_1D[data_1D.key_list[0]]["FLUX_wall"]))
    std = np.zeros(len(data_1D[data_1D.key_list[0]]["FLUX_wall"]))
    N = 0
    for i in range(0, len(data_1D.key_list)):
        try:
            diff = sum(
                abs(data_1D[data_1D.key_list[i]]["FLUX_wall"] - data_1D[data_1D.key_list[i + 1]]["FLUX_wall"])) / sum(
                abs(data_1D[data_1D.key_list[i]]["FLUX_wall"]))
        except:
            diff = np.nan  # in case
        df = data_1D[data_1D.key_list[i]]
        convergence.append(diff)
        if i >= plt_min:
            N += 1
            # ax1.plot(df["theta_wall"], df["FLUX_wall"])
            mean += -df["FLUX_wall"]

    mean = mean / N
    # Compute std
    for i in range(len(data_1D.key_list) - N, len(data_1D.key_list)):
        df = data_1D[data_1D.key_list[i]]
        std += (-df["FLUX_wall"] - mean) ** 2
    std = np.sqrt(std / N)

    plt.subplot(1, 2, 1)
    plt.title("Wall heat flux")
    lab = r"\begin{flushleft} $\mu$ on the \\" + str(
        round(data_1D.time[-1] - data_1D.time[plt_min], 2)) + " last seconds \end{flushleft}"
    ax1.plot(df["theta_wall"], mean, label=lab)
    ax1.fill_between(df["theta_wall"], y1=mean + std, y2=mean - std, alpha=0.5, color="r", label=r"$\mu$ +/- $\sigma$")
    ax1.annotate(r"$\bar{\sigma}$ = " + str(round(np.mean(std), 2)), (67.5, 30000), bbox=bbox)
    ax1.legend(loc="upper right")
    ax1.set_xlabel("$\Theta$ (deg)")
    ax1.set_ylabel("$q''$ (W/m$^2$) ")
    ax1.set_xticks([0, 45, 90, 135, 180])
    ax1.set_xlim([0.0, 180])
    #ax1.set_ylim(20000, 200000)
    ax1.grid(visible=True)

    plt.subplot(1, 2, 2)
    plt.title("Convergence")
    ax2.plot(data_1D.time, convergence)
    ax2.set_xlabel("Physical time (s)")
    ax2.set_ylabel(" $\ \int_{\partial \Omega _s}   |q''(t) - q''(t+1))| /  \int_{\partial \Omega _s}   |q''(t)| $")
    ax2.grid(visible=True)
    ax2.set_xlim((data_1D.time[0], data_1D.time[-1]))
    ax2.set_ylim((0, 1.0))
    savefig("heat_flux", format="png",pickle = fig ,dpi=1000)
    plt.show()

    # ***************************** Heat transfer coefficient

    '''fig, (ax1, ax2) = plt.subplots(1, 2)
    set_size(subplots=(1, 2))
    convergence = []  # check convergence
    mean = np.zeros(len(data_1D[data_1D.key_list[0]]["h_ws"]))
    std = np.zeros(len(data_1D[data_1D.key_list[0]]["h_ws"]))
    N = 0
    for i in range(0, len(data_1D.key_list)):
        try:
            diff = sum(
                abs(data_1D[data_1D.key_list[i]]["h_ws"] - data_1D[data_1D.key_list[i + 1]]["h_ws"])) / sum(
                abs(data_1D[data_1D.key_list[i]]["h_ws"]))
        except:
            diff = np.nan  # in case
        df = data_1D[data_1D.key_list[i]]
        convergence.append(diff)
        if i >= 180:
            N += 1
            # ax1.plot(df["theta_wall"], df["FLUX_wall"])
            mean += -df["h_ws"]

    mean = mean / N
    # Compute std
    for i in range(len(data_1D.key_list) - N, len(data_1D.key_list)):
        df = data_1D[data_1D.key_list[i]]
        std += (-df["h_ws"] - mean) ** 2
    std = np.sqrt(std / N)

    plt.subplot(1, 2, 1)
    plt.title("Heat transfer coefficient")
    ax1.plot(df["theta_wall"], mean, label=r"\begin{flushleft} $\mu$ on the \\ 20 last .plt \end{flushleft}")
    ax1.fill_between(df["theta_wall"], y1=mean + std, y2=mean - std, alpha=0.5, color="r", label=r"$\mu$ +/- $\sigma$")
    ax1.legend(loc="upper right")
    ax1.set_xlabel("$\Theta$ (deg)")
    ax1.set_ylabel("$h$ (W/m$^2$/K) ")
    ax1.annotate(r"$\bar{\sigma}$ = " + str(round(np.mean(std), 2)), (67.5, 100), bbox=bbox)
    ax1.grid(visible=True)
    ax1.set_xticks([0, 45, 90, 135, 180])
    ax1.set_xlim([0.0, 180])
    ax1.set_ylim((0, 900))

    plt.subplot(1, 2, 2)
    plt.title("Convergence")
    ax2.plot(data_1D.time, convergence)
    ax2.set_xlabel("Physical time (s)")
    ax2.set_ylabel(
        r' $ \int_{\partial \Omega _s}   |h_{w \to g}(t) - h_{w \to g}(t+1))| / \int_{\partial \Omega _s}   |h_{w \to g}(t)| $')
    ax2.grid(visible=True)
    ax2.set_xlim((data_1D.time[0], data_1D.time[-1]))
    ax2.set_ylim((0, 1.2))
    savefig("heat_transfer_coefficient", format="png", dpi=1000)
    plt.show()'''

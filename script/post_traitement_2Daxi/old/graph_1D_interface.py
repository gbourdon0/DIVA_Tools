from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from modules.post_proc_2D.convergence import convergence_1D
from scipy.interpolate import interp1d
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import seaborn as sns

import pandas as pd
import modules.diva_input as DIVA_in


'''paf = "/home/gbourdon/02_DIVA_benchmark_drag/11_5d-1/post_traitement"
configure_latex(style="seaborn-bright", global_save_path=paf + "/images")'''
bbox = dict(boxstyle="round", fc="1")

'''# load data
DIVA_input = DIVA_in.diva_input()
DIVA_input.load("/home/gbourdon/02_DIVA_benchmark_drag/11_5d-1//run")
time = pd.read_csv(paf + "/time.csv", sep=";")
time = np.array(time["time (s)"])

interface = pr()
interface.load_folder("/home/gbourdon/02_DIVA_benchmark_drag/11_5d-1/post_traitement/data1D/interface")
interface.define_time(time)  # Associated a time list with the data
print(interface.get_header())'''

from scipy.interpolate import interp1d



def interface_heat_flux(interface, time, theta_max):
    theta = np.arange(2, theta_max, 1)
    # ********************* Evaporation flux
    convergence, mean, std, idx = convergence_1D(interface, "theta_interface", "FLUX_evap", theta, t_start_time=time)
    # color negative value
    color = []
    for elem in mean:
        if elem < 0:
            color.append(elem)
        else:
            color.append(np.nan)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    set_size(subplots=(1, 2))
    # First plot
    plt.subplot(1, 2, 1)
    lab = r"\begin{flushleft} $\mu$ on the \\" + str(
        round(interface.time[-1] - interface.time[idx], 2)) + " last seconds \end{flushleft}"
    ax1.plot(theta, mean, label=lab)
    ax1.plot(theta, color, color="r", label="Condensation")
    ax1.fill_between(theta, y1=(mean + std), y2=(mean - std), alpha=0.5, color="r",
                     label=r"$\mu$ +/- $\sigma$")
    plt.title("Evaporation Flux")
    ax1.set_xlabel("$\Theta$ (deg)")
    ax1.set_ylabel("$q''_{evap}$ (W/m$^2$) ")
    ax1.legend(loc="upper right")
    ax1.set_xlim([0, 180])
    ax1.grid(visible=True)
    
    # Second plot
    plt.subplot(1, 2, 2)
    ax2.plot(interface.time, convergence)
    plt.title("Convergence")
    ax2.set_xlabel("Physical time (s)")
    ax2.set_ylabel(" $\int_{\Gamma}   |q''(t) - q'' _{evap}(t+dt))| /  \int_{\Gamma}   |q'' _{evap}(t)| $")
    ax2.set_xlim((interface.time[0], interface.time[-1]))
    ax2.set_ylim(0, 1)
    ax2.grid(visible=True)
    savefig("evap_flux", format="png",pickle = fig, dpi=1000)
    plt.show()
    
    # ********************* flux liq
    convergence, mean, std, idx = convergence_1D(interface, "theta_interface", "FLUX_liq", theta,t_start_time=time)
    # color negative value
    fig, (ax1, ax2) = plt.subplots(1, 2)
    set_size(subplots=(1, 2))
    # First plot
    plt.subplot(1, 2, 1)
    lab = r"\begin{flushleft} $\mu$ on the \\" + str(
        round(interface.time[-1] - interface.time[idx], 2)) + " last seconds \end{flushleft}"
    ax1.plot(theta, mean, label=lab)
    ax1.fill_between(theta, y1=(mean + std), y2=(mean - std), alpha=0.5, color="r",
                     label=r"$\mu$ +/- $\sigma$")
    plt.title("Liquid Heat Flux")
    ax1.set_xlabel("$\Theta$ (deg)")
    ax1.set_ylabel("$q''$ (W/m$^2$) ")
    ax1.set_xticks([0, 45, 90, 135, 180])
    ax1.legend(loc="upper right")
    ax1.set_xlim([0, 180])
    ax1.grid(visible=True)
    
    # Second plot
    plt.subplot(1, 2, 2)
    ax2.plot(interface.time, convergence)
    plt.title("Convergence")
    ax2.set_xlabel("Physical time (s)")
    ax2.set_ylabel(" $\int_{\Gamma}   |q'' (t) - q''(t+dt))| /  \int_{\Gamma}   |q'' (t)| $")
    ax2.set_xlim((interface.time[0], interface.time[-1]))
    ax2.set_ylim(0, 1)
    ax2.grid(visible=True)
    savefig("liquid_flux", format="png",pickle = fig, dpi=1000)
    plt.show()
    
    # ********************* flux gas
    convergence, mean, std, idx = convergence_1D(interface, "theta_interface", "FLUX_gas", theta, t_start_time=time)
    # color negative value
    fig, (ax1, ax2) = plt.subplots(1, 2)
    set_size(subplots=(1, 2))
    # First plot
    plt.subplot(1, 2, 1)
    lab = r"\begin{flushleft} $\mu$ on the \\" + str(
        round(interface.time[-1] - interface.time[idx], 2)) + " last seconds \end{flushleft}"
    ax1.plot(theta, mean, label=lab)
    ax1.fill_between(theta, y1=(mean + std), y2=(mean - std), alpha=0.5, color="r",
                     label=r"$\mu$ +/- $\sigma$")
    plt.title("Gas Heat Flux")
    ax1.set_xlabel("$\Theta$ (deg)")
    ax1.set_ylabel("$q''$ (W/m$^2$) ")
    ax1.legend(loc="upper right")
    ax1.set_xlim([0, 180])
    ax1.grid(visible=True)
    
    # Second plot
    plt.subplot(1, 2, 2)
    ax2.plot(interface.time, convergence)
    plt.title("Convergence")
    ax2.set_xlabel("Physical time (s)")
    ax2.set_ylabel(" $\int_{\Gamma}   |q''(t) - q'' (t+dt))| /  \int_{\Gamma}   |q'' (t)| $")
    ax2.set_xlim((interface.time[0], interface.time[-1]))
    ax2.set_ylim(0, 1)
    ax2.grid(visible=True)
    savefig("gas_flux", format="png", pickle = fig,dpi=1000)
    plt.show()

from modules.data_reader.pickle_reader import PickleReader as pr
from modules.data_reader.read_dat import read_dat
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import seaborn as sns
from modules.usefull_functions.functions import *
import pandas as pd
import modules.diva_input as DIVA_in

########################################################################################################################
#                                       Loading data
########################################################################################################################
# Input
#paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
#paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
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
int_heat_flux = read_dat(paf + "run/Data/Heat_flux.dat")

########################################################################################################################
#                                       DETECT SIGNAL PERIOD
########################################################################################################################
# Input
print("Do not forget to change input in the DETECT SIGNAL PERIOD")
SAMPLE_RATE = 2000
FIELD_dat = "Interface_evap_heat_flux"
FIELD_pickle = "FLUX_evap"
FILENAME = "EHF"
T_START1 = 0.25
N_PERIOD = 1

int_heat_flux = int_heat_flux.loc[int_heat_flux["t(s)"]>=T_START1]
def period(plot=True):
    """
    perform FFT of the temporal integrated signal to get periodic motion.
    :return: the biggest period of the signal (except the 0 frequency one i.e the infinite perdiod)
    """
    from modules.signal_treatment.FFT import FFT, threshold_filter
    # Do the math

    (PSD, freq, PSD_plot, freq_plot, f_hat, t) = FFT(int_heat_flux["t(s)"], int_heat_flux[FIELD_dat], sr=SAMPLE_RATE)
    f_max, amp_max = maximums(freq_plot, PSD_plot, max_number=100)
    print(f_max)
    val_max,fmin = minimums(amp_max,f_max, max_number=2)
    fmin= fmin[1]
    print(fmin)
    PSD_filter,f_hat_filter = threshold_filter(f_hat,PSD, min(amp_max))
    f_filter = np.fft.ifft(f_hat_filter)

    if plot:
        # Figure
        fig, ax1 = plt.subplots(1)
        ax1.plot(int_heat_flux["t(s)"], int_heat_flux[FIELD_dat], label="original")
        ax1.plot(t, f_filter, label=f"IFFT with the {len(f_max)} frequencies. Biggest non zero frequency :{fmin:.2f}")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(r'$\bar{q^{''}}$ (W/m$^2$)')
        ax1.grid(visible=True)
        ax1.legend()
        savefig(file_name=FILENAME + "_integrated", format="png", pickle=fig, dpi=1000)
        plt.show()

        fig, ax1 = plt.subplots(1)
        ax1.fill_between(freq_plot, y1=[0] * len(PSD_plot), y2=PSD_plot, alpha=.5, color="r")
        ax1.scatter(f_max, amp_max, marker="x")
        ax1.set_xlabel("Frequency (Hz)")
        ax1.set_ylabel(r'FFT Amplitude $|X(freq)|^2$')
        ax1.set_yscale('log')
        ax1.grid(visible=True)
        ax1.set_xlim(0, max(freq_plot))
        savefig(FILENAME + "_FFT", format="png", pickle=fig, dpi=1000)

        plt.show()


    return (1 / fmin)


T = period(plot=DEBUG)

print(f"Period is {T:.2} s")
########################################################################################################################
#                                       PERIOD AVERAGE VALUES
########################################################################################################################
# Input
print("Do not forget to fill input in the PERIOD AVERAGE VALUES")
T_START = T_START1
# Computation of integration range
T_START,idx_start = nearest_value(time, T_START)
T_END = T_START + T*N_PERIOD

if T_END>time[-1]:
    raise Exception("Borne sup for integration time is ou the maximum time value. Please reduce N_PERIOD")
T_END, idx_end = nearest_value(time, T_END)

if DEBUG:
    plt.plot(int_heat_flux["t(s)"], int_heat_flux[FIELD_dat])
    y_min,y_max = min(int_heat_flux[FIELD_dat]),max(int_heat_flux[FIELD_dat])
    plt.vlines(T_START,y_min,y_max)
    plt.vlines(T_END,y_min,y_max)
    plt.show()
DT = T_END - T_START
print(
    f"The integration time with respect with time discretization is {T_END - T_START:.2} s. Difference with the wished one is "
    f"{abs(N_PERIOD*T - DT) / (N_PERIOD*T) * 100:.2} %.")


theta = np.arange(0,180,1)
time_avg_flux = np.zeros(len(theta))


for i in range(idx_start+1,idx_end+1):
    dt = time[i]-time[i-1]
    f = interp1d(wall[wall.key_list[i]]["theta_interface"],wall[wall.key_list[i]][FIELD_pickle], kind = 'linear',bounds_error = False, fill_value=np.nan)
    time_avg_flux += f(theta)*dt

time_avg_flux /= DT
fig,ax1 = plt.subplots()

time_std_flux = np.zeros(len(theta))
for i in range(idx_start+1,idx_end+1):
    dt = time[i] - time[i - 1]
    f = interp1d(wall[wall.key_list[i]]["theta_interface"], wall[wall.key_list[i]][FIELD_pickle], kind = 'linear',bounds_error = False,fill_value=np.nan )
    time_std_flux += (f(theta)-time_avg_flux)**2*dt
time_std_flux = np.sqrt(time_std_flux/DT)


ax1.plot(theta,time_avg_flux, label = r"$\mu$")
ax1.fill_between(theta, y1=(time_avg_flux + time_std_flux), y2=(time_avg_flux - time_std_flux) , alpha=0.5, color="r",label=r"$\mu$ +/- $\sigma$")
ax1.set_xlim(0,180)
ax1.set_xlabel(r"$\theta$ (deg)")
ax1.set_ylabel(r"q'' (W/m$^2$)")
ax1.grid(visible=True)
plt.legend()
savefig(FILENAME + "_avg", format="png", pickle=fig, dpi=1000)
plt.show()
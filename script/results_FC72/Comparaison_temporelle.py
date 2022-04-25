from modules.data_reader.pickle_plt import PicklePLT
import matplotlib.pyplot as plt
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
from scipy.interpolate import interp1d
import numpy as np
import modules.diva_input as DIVA_in
from modules.data_reader.read_dat import read_dat
configure_latex(style="seaborn-bright", global_save_path="/work/gbourdon/02_benchmark_FC72/COMPARAISON")
paf_liste = [
"/work/gbourdon/02_benchmark_FC72/13_0/",
"/work/gbourdon/02_benchmark_FC72/06_1d-1/",
"/work/gbourdon/02_benchmark_FC72/07_2d-1/",
"/work/gbourdon/02_benchmark_FC72/08_3d-1/",
"/work/gbourdon/02_benchmark_FC72/09_4d-1/",
"/work/gbourdon/02_benchmark_FC72/11_5d-1/"]
legend_text = ["0.0 m/s", "0.1 m/s", "0.2 m/s", "0.3 m/s", "0.4 m/s", "0.5 m/s"]


########################################################################################################################
#                                       READING FILES
########################################################################################################################


paf_liste = [paf_liste[i]+"run/Data/Heat_flux.dat" for i in range(len(paf_liste))]

filelist = [read_dat(paf) for paf in paf_liste]
print(filelist[0].columns)


########################################################################################################################
#                                      WHF
########################################################################################################################

fig,ax = plt.subplots()
for i in range(len(filelist)):
    df = filelist[i]
    ax.plot(df["t(s)"],abs(df["Wall_heat_flux"]), label = legend_text[i])

ax.set_xlabel("time (s)")
ax.set_ylabel(r"q'' (W/m$^2$)")
ax.set_xlim(0.2,0.5)
ax.set_ylim(60000,120000)
ax.grid(True)
plt.legend()
savefig("WHF_temporal_comp", format="png", dpi=1000)
plt.show()

########################################################################################################################
#                                      EHF
########################################################################################################################
fig,ax = plt.subplots()
for i in range(len(filelist)):
    df = filelist[i]
    ax.plot(df["t(s)"],abs(df["Interface_evap_heat_flux"]), label = legend_text[i])

ax.set_xlabel("time (s)")
ax.set_ylabel(r"q'' (W/m$^2$)")
ax.set_xlim(0.35,0.5)
ax.set_ylim(10000,40000)
ax.grid(True)
plt.legend()
savefig("EHF_temporal_comp", format="png", dpi=1000)
plt.show()


########################################################################################################################
#                                      Interface_liq_heat_Flux
########################################################################################################################
fig,ax = plt.subplots()
for i in range(len(filelist)):
    df = filelist[i]
    ax.plot(df["t(s)"],abs(df["Interface_liq_heat_Flux"]), label = legend_text[i])

ax.set_xlabel("time (s)")
ax.set_ylabel(r"q'' (W/m$^2$)")
ax.set_xlim(0.35,0.5)
ax.set_ylim(0,4e7)
ax.grid(True)
plt.legend()
savefig("LHF_temporal_comp", format="png", dpi=1000)
plt.show()
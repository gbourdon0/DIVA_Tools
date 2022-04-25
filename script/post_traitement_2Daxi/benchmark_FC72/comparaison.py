from modules.data_reader.pickle_plt import PicklePLT
import matplotlib.pyplot as plt
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig

configure_latex(style="seaborn-bright", global_save_path="/work/gbourdon/02_benchmark_FC72/COMPARAISON")

# ***********************************************************************************************************************
#                                       Comparaison film thickness
# ***********************************************************************************************************************
# ----- LOAD DATA

pc0 = PicklePLT()
pc1 = PicklePLT()
pc2 = PicklePLT()
pc3 = PicklePLT()
pc4 = PicklePLT()
pc5 = PicklePLT()

paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
fig0, axes0 = pc0.load_pickle(path=paf + "post_traitement/images/e_film.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
fig1, axes1 = pc1.load_pickle(path=paf + "post_traitement/images/e_film.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
fig2, axes2 = pc2.load_pickle(path=paf + "post_traitement/images/e_film.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
fig3, axes3 = pc3.load_pickle(path=paf + "post_traitement/images/e_film.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
fig4, axes4 = pc4.load_pickle(path=paf + "post_traitement/images/e_film.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
fig5, axes5 = pc5.load_pickle(path=paf + "post_traitement/images/e_film.pickle")

plt.clf()
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)
plt.close(fig0)

pc0.get_data_header()

# ----- FILM THICKNESS TOT
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 1)
ax.plot(x0, y0, label="0 m/s")
x0, yf0_up, yf0_down = pc0.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

x1, y1 = pc1.get_data(0, 1)
ax.plot(x1, y1, label="0.1 m/s")
x1, yf1_up, yf1_down = pc1.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x1, yf1_up, yf1_down, alpha=0.4)

x2, y2 = pc2.get_data(0, 1)
ax.plot(x2, y2, label="0.2 m/s")
x2, yf2_up, yf2_down = pc2.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x2, yf2_up, yf2_down, alpha=0.4)

x3, y3 = pc3.get_data(0, 1)
ax.plot(x3, y3, label="0.3 m/s")
x3, yf3_up, yf3_down = pc3.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x3, yf3_up, yf3_down, alpha=0.4)

x4, y4 = pc4.get_data(0, 1)
ax.plot(x4, y4, label="0.4 m/s")
x4, yf4_up, yf4_down = pc4.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x4, yf4_up, yf4_down, alpha=0.4)

x5, y5 = pc5.get_data(0, 1)
ax.plot(x5, y5, label="0.5 m/s")
x5, yf5_up, yf5_down = pc5.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x5, yf5_up, yf5_down, alpha=0.4)

ax.legend(loc="upper left")
ax.grid(visible=True)
ax.set_xlabel("$\Theta$ (deg)")
ax.set_ylabel("$e_{film}$ (mm) ")
ax.set_xlim(0, 170)
ax.set_ylim(0, 18)
savefig("thickness", format="png", dpi=1000)
#plt.show()
plt.close()


# ----- FILM THICKNESS ZOOM
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 1)
ax.plot(x0, y0, label="0 m/s")
x0, yf0_up, yf0_down = pc0.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

x1, y1 = pc1.get_data(0, 1)
ax.plot(x1, y1, label="0.1 m/s")
x1, yf1_up, yf1_down = pc1.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x1, yf1_up, yf1_down, alpha=0.4)

x2, y2 = pc2.get_data(0, 1)
ax.plot(x2, y2, label="0.2 m/s")
x2, yf2_up, yf2_down = pc2.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x2, yf2_up, yf2_down, alpha=0.4)

x3, y3 = pc3.get_data(0, 1)
ax.plot(x3, y3, label="0.3 m/s")
x3, yf3_up, yf3_down = pc3.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x3, yf3_up, yf3_down, alpha=0.4)

x4, y4 = pc4.get_data(0, 1)
ax.plot(x4, y4, label="0.4 m/s")
x4, yf4_up, yf4_down = pc4.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x4, yf4_up, yf4_down, alpha=0.4)

x5, y5 = pc5.get_data(0, 1)
ax.plot(x5, y5, label="0.5 m/s")
x5, yf5_up, yf5_down = pc5.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x5, yf5_up, yf5_down, alpha=0.4)

ax.legend(loc="upper left")
ax.grid(visible=True)
ax.set_xlabel("$\Theta$ (deg)")
ax.set_ylabel("$e_{film}$ (mm) ")
ax.set_xlim(0, 135)
ax.set_ylim(0, 4)
savefig("thickness_zoom", format="png", dpi=1000)
#plt.show()
plt.close()

# ***********************************************************************************************************************
#                                       WALL HEAT FLUX
# ***********************************************************************************************************************

# ----- LOAD DATA

pc0 = PicklePLT()
pc1 = PicklePLT()
pc2 = PicklePLT()
pc3 = PicklePLT()
pc4 = PicklePLT()
pc5 = PicklePLT()

paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
fig0, axes0 = pc0.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
fig1, axes1 = pc1.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
fig2, axes2 = pc2.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
fig3, axes3 = pc3.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
fig4, axes4 = pc4.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
fig5, axes5 = pc5.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

plt.clf()
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)
plt.close(fig0)

pc0.get_data_header()

# ----- WALL HEAT FLUX TOT
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 0)
ax.plot(x0, y0, label="0 m/s")
x0, yf0_up, yf0_down = pc0.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

x1, y1 = pc1.get_data(0, 0)
ax.plot(x1, y1, label="0.1 m/s")
x1, yf1_up, yf1_down = pc1.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x1, yf1_up, yf1_down, alpha=0.4)

x2, y2 = pc2.get_data(0, 0)
ax.plot(x2, y2, label="0.2 m/s")
x2, yf2_up, yf2_down = pc2.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x2, yf2_up, yf2_down, alpha=0.4)

x3, y3 = pc3.get_data(0, 0)
ax.plot(x3, y3, label="0.3 m/s")
x3, yf3_up, yf3_down = pc3.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x3, yf3_up, yf3_down, alpha=0.4)

x4, y4 = pc4.get_data(0, 0)
ax.plot(x4, y4, label="0.4 m/s")
x4, yf4_up, yf4_down = pc4.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x4, yf4_up, yf4_down, alpha=0.4)

x5, y5 = pc5.get_data(0, 0)
ax.plot(x5, y5, label="0.5 m/s")
x5, yf5_up, yf5_down = pc5.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x5, yf5_up, yf5_down, alpha=0.4)

ax.legend(loc="upper right")
ax.grid(visible=True)
ax.set_xlabel("$\Theta$ (deg)")
ax.set_ylabel(r"Wall heat flux (W/m$^2$)")
ax.set_xlim(0, 170)
ax.set_ylim(0, 200000)
savefig("WHF", format="png", dpi=1000)
#plt.show()
plt.close()


# ***********************************************************************************************************************
#                                       WALL HEAT FLUX AND FILM THICKNESS
# ***********************************************************************************************************************

# ----- LOAD DATA

pc0 = PicklePLT()
pc1 = PicklePLT()
pc2 = PicklePLT()
pc3 = PicklePLT()
pc4 = PicklePLT()
pc5 = PicklePLT()

paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
fig0, axes0 = pc0.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
fig1, axes1 = pc1.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
fig2, axes2 = pc2.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
fig3, axes3 = pc3.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
fig4, axes4 = pc4.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
fig5, axes5 = pc5.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")

plt.clf()
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)
plt.close(fig0)

pc0.get_data_header()

# ----- WALL HEAT FLUX TOT
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 0)
ax.plot(x0, y0, label="0 m/s")


x1, y1 = pc1.get_data(0, 0)
ax.plot(x1, y1, label="0.1 m/s")


x2, y2 = pc2.get_data(0, 0)
ax.plot(x2, y2, label="0.2 m/s")


x3, y3 = pc3.get_data(0, 0)
ax.plot(x3, y3, label="0.3 m/s")

x4, y4 = pc4.get_data(0, 0)
ax.plot(x4, y4, label="0.4 m/s")


x5, y5 = pc5.get_data(0, 0)
ax.plot(x5, y5, label="0.5 m/s")


ax.legend(loc="upper right")
ax.grid(visible=True)
ax.set_ylabel(r"Wall heat flux (W/m$^2$)")
ax.set_xlabel(r"Film thickness (mm)")
ax.set_xlim(0, 170)
ax.set_ylim(0, 200000)
savefig("WHF_TCK", format="png", dpi=1000)
#plt.show()
plt.close()

# ***********************************************************************************************************************
#                                       GAS HEAT FLUX
# ***********************************************************************************************************************

# ----- LOAD DATA

pc0 = PicklePLT()
pc1 = PicklePLT()
pc2 = PicklePLT()
pc3 = PicklePLT()
pc4 = PicklePLT()
pc5 = PicklePLT()

paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
fig0, axes0 = pc0.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
fig1, axes1 = pc1.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
fig2, axes2 = pc2.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
fig3, axes3 = pc3.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
fig4, axes4 = pc4.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
fig5, axes5 = pc5.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")

plt.clf()
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)
plt.close(fig0)

pc0.get_data_header()

# ----- WALL HEAT FLUX TOT
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 0)
ax.plot(x0, y0, label="0 m/s")
x0, yf0_up, yf0_down = pc0.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

x1, y1 = pc1.get_data(0, 0)
ax.plot(x1, y1, label="0.1 m/s")
x1, yf1_up, yf1_down = pc1.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x1, yf1_up, yf1_down, alpha=0.4)

x2, y2 = pc2.get_data(0, 0)
ax.plot(x2, y2, label="0.2 m/s")
x2, yf2_up, yf2_down = pc2.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x2, yf2_up, yf2_down, alpha=0.4)

x3, y3 = pc3.get_data(0, 0)
ax.plot(x3, y3, label="0.3 m/s")
x3, yf3_up, yf3_down = pc3.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x3, yf3_up, yf3_down, alpha=0.4)

x4, y4 = pc4.get_data(0, 0)
ax.plot(x4, y4, label="0.4 m/s")
x4, yf4_up, yf4_down = pc4.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x4, yf4_up, yf4_down, alpha=0.4)

x5, y5 = pc5.get_data(0, 0)
ax.plot(x5, y5, label="0.5 m/s")
x5, yf5_up, yf5_down = pc5.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x5, yf5_up, yf5_down, alpha=0.4)


ax.legend(loc="upper right")
ax.grid(visible=True)
ax.set_ylabel(r"Gas heat flux (W/m$^2$)")
ax.set_xlabel("$\Theta$ (deg)")
ax.set_xlim(0, 170)
ax.set_ylim(-100000,300000)
savefig("GHF", format="png", dpi=1000)
#plt.show()
plt.close()


# ***********************************************************************************************************************
#                                       LIQUID HEAT FLUX
# ***********************************************************************************************************************

# ----- LOAD DATA

pc0 = PicklePLT()
pc1 = PicklePLT()
pc2 = PicklePLT()
pc3 = PicklePLT()
pc4 = PicklePLT()
pc5 = PicklePLT()

paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
fig0, axes0 = pc0.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
fig1, axes1 = pc1.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
fig2, axes2 = pc2.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
fig3, axes3 = pc3.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
fig4, axes4 = pc4.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
fig5, axes5 = pc5.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")

plt.clf()
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)
plt.close(fig0)

pc0.get_data_header()

# ----- WALL HEAT FLUX TOT
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 0)
ax.plot(x0, y0, label="0 m/s")
x0, yf0_up, yf0_down = pc0.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

x1, y1 = pc1.get_data(0, 0)
ax.plot(x1, y1, label="0.1 m/s")
x1, yf1_up, yf1_down = pc1.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x1, yf1_up, yf1_down, alpha=0.4)

x2, y2 = pc2.get_data(0, 0)
ax.plot(x2, y2, label="0.2 m/s")
x2, yf2_up, yf2_down = pc2.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x2, yf2_up, yf2_down, alpha=0.4)

x3, y3 = pc3.get_data(0, 0)
ax.plot(x3, y3, label="0.3 m/s")
x3, yf3_up, yf3_down = pc3.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x3, yf3_up, yf3_down, alpha=0.4)

x4, y4 = pc4.get_data(0, 0)
ax.plot(x4, y4, label="0.4 m/s")
x4, yf4_up, yf4_down = pc4.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x4, yf4_up, yf4_down, alpha=0.4)

x5, y5 = pc5.get_data(0, 0)
ax.plot(x5, y5, label="0.5 m/s")
x5, yf5_up, yf5_down = pc5.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x5, yf5_up, yf5_down, alpha=0.4)


ax.legend(loc="lower left")
ax.grid(visible=True)
ax.set_ylabel(r"Liquid heat flux (W/m$^2$)")
ax.set_xlabel("$\Theta$ (deg)")
ax.set_xlim(0, 170)
ax.set_ylim(-400,600)
savefig("LHF", format="png", dpi=1000)
#plt.show()
plt.close()

# ***********************************************************************************************************************
#                                       EVAPORATION HEAT FLUX
# ***********************************************************************************************************************

# ----- LOAD DATA

pc0 = PicklePLT()
pc1 = PicklePLT()
pc2 = PicklePLT()
pc3 = PicklePLT()
pc4 = PicklePLT()
pc5 = PicklePLT()

paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
fig0, axes0 = pc0.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
fig1, axes1 = pc1.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
fig2, axes2 = pc2.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
fig3, axes3 = pc3.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
fig4, axes4 = pc4.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")

paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
fig5, axes5 = pc5.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")

plt.clf()
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)
plt.close(fig0)

pc0.get_data_header()

# ----- WALL HEAT FLUX TOT
fig, ax = plt.subplots(1)
x0, y0 = pc0.get_data(0, 0)
ax.plot(x0, y0, label="0 m/s")
x0, yf0_up, yf0_down = pc0.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

x1, y1 = pc1.get_data(0, 0)
ax.plot(x1, y1, label="0.1 m/s")
x1, yf1_up, yf1_down = pc1.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x1, yf1_up, yf1_down, alpha=0.4)

x2, y2 = pc2.get_data(0, 0)
ax.plot(x2, y2, label="0.2 m/s")
x2, yf2_up, yf2_down = pc2.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x2, yf2_up, yf2_down, alpha=0.4)

x3, y3 = pc3.get_data(0, 0)
ax.plot(x3, y3, label="0.3 m/s")
x3, yf3_up, yf3_down = pc3.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x3, yf3_up, yf3_down, alpha=0.4)

x4, y4 = pc4.get_data(0, 0)
ax.plot(x4, y4, label="0.4 m/s")
x4, yf4_up, yf4_down = pc4.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x4, yf4_up, yf4_down, alpha=0.4)

x5, y5 = pc5.get_data(0, 0)
ax.plot(x5, y5, label="0.5 m/s")
x5, yf5_up, yf5_down = pc5.get_data(0, "$\\mu$ +/- $\\sigma$")
ax.fill_between(x5, yf5_up, yf5_down, alpha=0.4)


ax.legend(loc="lower left")
ax.grid(visible=True)
ax.set_ylabel(r"Evaporation heat flux (W/m$^2$)")
ax.set_xlabel("$\Theta$ (deg)")
ax.set_xlim(0, 170)
ax.set_ylim(-50000,300000)
savefig("EHF", format="png", dpi=1000)
plt.show()
plt.close()
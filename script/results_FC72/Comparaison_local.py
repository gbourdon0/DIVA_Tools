from modules.data_reader.pickle_plt import PicklePLT
import matplotlib.pyplot as plt
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
from scipy.interpolate import interp1d
import numpy as np
import modules.diva_input as DIVA_in

configure_latex(style="seaborn-bright", global_save_path="/work/gbourdon/02_benchmark_FC72/COMPARAISON")
paf_liste = [
"/work/gbourdon/02_benchmark_FC72/13_0/",
"/work/gbourdon/02_benchmark_FC72/06_1d-1/",
"/work/gbourdon/02_benchmark_FC72/07_2d-1/",
"/work/gbourdon/02_benchmark_FC72/08_3d-1/",
"/work/gbourdon/02_benchmark_FC72/09_4d-1/",
"/work/gbourdon/02_benchmark_FC72/11_5d-1/"]
legend_text = ["0.0 m/s", "0.1 m/s", "0.2 m/s", "0.3 m/s", "0.4 m/s", "0.5 m/s"]

def load_fig(paf_list):
    """
    A simple function to load matplotlib figure object save in a .pickle file
    :param paf_list: path of differents figure
    :return: fig_list[i] = (fig,ax) of the i-th path
    """
    fig_list = []
    for paf in paf_list:
        pc0 = PicklePLT()
        fig0, axes0 = pc0.load_pickle(path=paf)
        fig_list.append(pc0)

        plt.clf()
        plt.close(fig0)
    print(pc0.get_data_header())
    return fig_list

########################################################################################################################
#                                           FILM THICKNESS
########################################################################################################################
def film_thickness():
    thick_list = [p  +"post_traitement/images/FT_avg.pickle" for p in paf_liste]
    figures = load_fig(thick_list)

    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0,y0 = figures[i].get_data(0, 0)

        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

    ax.legend(loc="upper left")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel("$e_{film}$ (mm) ")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 35)
    savefig("Thickness_comp", format="png", dpi=1000)
    plt.show()

    # ZOOM
    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0,y0 = figures[i].get_data(0, 0)

        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)
    ax.legend(loc="upper left")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel("$e_{film}$ (mm) ")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 2.5)
    savefig("Thickness_comp_ZOOM", format="png", dpi=1000)
    plt.show()
    # plt.close()

#film_thickness()
########################################################################################################################
#                                           WALL HEAT FLUX
########################################################################################################################
def WHF():
    thick_list = [p + "post_traitement/images/WHF_avg.pickle" for p in paf_liste]
    figures = load_fig(thick_list)

    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0, y0 = figures[i].get_data(0, 0)
        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_down, yf0_up, alpha=0.4)

    ax.legend(loc="upper right")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel("q'' (W/m$^2$)")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 200000)
    savefig("WHF_comp", format="png", dpi=1000)
    plt.show()
    plt.close()

#WHF()

########################################################################################################################
#                                           WALL HEAT FLUX = f(thickness)
########################################################################################################################
def WHF_thickness():

    thick_list = [p + "post_traitement/images/WHF_avg.pickle" for p in paf_liste]
    figures_WHF = load_fig(thick_list)
    thick_list = [p + "post_traitement/images/FT_avg.pickle" for p in paf_liste]
    figures_THICK = load_fig(thick_list)
    input_list = [p + "run" for p in paf_liste]

    fig, ax = plt.subplots()
    for i in range(len(figures_WHF)):
        x0, y0 = figures_WHF[i].get_data(0, 0)
        x1, y1 = figures_THICK[i].get_data(0, 0)

        xx0, yf0_up, yf0_down = figures_WHF[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        std0 = (yf0_up +yf0_down)/2
        xx1, yf1_up, yf1_down = figures_WHF[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        std1 = (yf1_up +yf1_down)/2
        #ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)
        f_WHF = interp1d(x0,y0, kind = 'linear',bounds_error = False, fill_value=np.nan)
        f_thick = interp1d(x1,y1, kind = 'linear',bounds_error = False, fill_value=np.nan)
        f_WHF_std = interp1d(xx0,std0, kind = 'linear',bounds_error = False, fill_value=np.nan)
        f_thick_std = interp1d(xx1,std1, kind = 'linear',bounds_error = False, fill_value=np.nan)
        theta = np.arange(3,177,1)
        x_plot = f_thick(theta)
        y_plot = f_WHF(theta)
        WHF_std = f_WHF_std(theta)
        Thick_std = f_thick_std(theta)
        ax.plot(x_plot, y_plot, label=legend_text[i])
        #ax.errorbar(x_plot,y_plot,xerr =Thick_std,yerr=WHF_std )

    DIVA_input = DIVA_in.diva_input()
    DIVA_input.load(input_list[i])
    cond = DIVA_input.TP.kth_vap * (DIVA_input.IC.T_immersed - DIVA_input.TP.t_sat) / x_plot * 1000
    ax.plot(x_plot, cond,linestyle= "--", color = "k", label="Pure conduction flux")
    ax.legend(loc="upper right")
    ax.grid(visible=True)
    ax.set_xlabel("$e_{film}$ (mm) ")
    ax.set_ylabel("q'' (W/m$^2$)")
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 180000)
    savefig("WHF_Thick_comp", format="png", dpi=1000)
    plt.show()
    plt.close()

#WHF_thickness()

########################################################################################################################
#                                           GAS HEAT FLUX
########################################################################################################################
def GHF():
    thick_list = [p + "post_traitement/images/GHF_avg.pickle" for p in paf_liste]
    figures = load_fig(thick_list)

    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0, y0 = figures[i].get_data(0, 0)
        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

    ax.legend(loc="upper right")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel("q'' (W/m$^2$)")
    ax.set_xlim(0, 180)
    ax.set_ylim(-50000, 300000)
    savefig("GHF_comp", format="png", dpi=1000)
    plt.show()
    plt.close()

#GHF()


########################################################################################################################
#                                           LIQUID HEAT FLUX
########################################################################################################################
def LHF():
    thick_list = [p + "post_traitement/images/LHF_avg.pickle" for p in paf_liste]
    figures = load_fig(thick_list)

    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0, y0 = figures[i].get_data(0, 0)
        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

    ax.legend(loc="upper left")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel("q'' (W/m$^2$)")
    ax.set_xlim(0, 180)
    ax.set_ylim(-500, 1500)
    savefig("LHF_comp", format="png", dpi=1000)
    plt.show()
    plt.close()

#LHF()

########################################################################################################################
#                                          EVAPORATION HEAT FLUX
########################################################################################################################
def EHF():
    thick_list = [p + "post_traitement/images/EHF_avg.pickle" for p in paf_liste]
    figures = load_fig(thick_list)

    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0, y0 = figures[i].get_data(0, 0)
        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

    ax.legend(loc="upper right")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel("q'' (W/m$^2$)")
    ax.set_xlim(0, 180)
    ax.set_ylim(-50000, 300000)
    savefig("EHF_comp", format="png", dpi=1000)
    plt.show()
    plt.close()

#EHF()

########################################################################################################################
#                                          GradP_r
########################################################################################################################
def gradP_r():

    thick_list = [p + "post_traitement/images/gradP_avg.pickle" for p in paf_liste]
    print("WARNING : gradP_r exclude last simulation in the list !!!!!!!!!!!!!")
    thick_list = thick_list[:-1]
    figures = load_fig(thick_list)

    fig, ax = plt.subplots()
    for i in range(len(figures)):
        x0, y0 = figures[i].get_data(0, 0)
        ax.plot(x0, y0, label=legend_text[i])
        x0, yf0_up, yf0_down = figures[i].get_data(0, "$\\mu$ +/- $\\sigma$")
        ax.fill_between(x0, yf0_up, yf0_down, alpha=0.4)

    ax.legend(loc="upper left")
    ax.grid(visible=True)
    ax.set_xlabel("$\Theta$ (deg)")
    ax.set_ylabel(r"$\nabla P_r$ (Pa/m)")
    ax.set_xlim(0, 110)
    ax.set_ylim(-500, 2500)
    savefig("GradP_comp", format="png", dpi=1000)
    plt.show()
    plt.close()

gradP_r()
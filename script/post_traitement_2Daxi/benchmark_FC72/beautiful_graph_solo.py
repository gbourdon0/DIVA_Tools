from modules.data_reader.pickle_plt import PicklePLT
import matplotlib.pyplot as plt
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import matplotlib

# 0 m/s
def run():
    paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
    configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/graph_presentation")
    import os
    try:
        os.mkdir(paf + "post_traitement/graph_presentation")
    except:
        pass

    # Thickness
    thickness = PicklePLT()
    fig, axes = thickness.load_pickle(path=paf + "post_traitement/images/e_film.pickle")
    axes[0].set_ylim(0, 14)
    savefig("e_film", format="png", dpi=1000)
    plt.show()

    # Wall heat flux =
    whf = PicklePLT()
    fig, axes = whf.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")
    whf.move_annotation(label = '',x= 45)
    axes[0].legend(loc="lower left")
    savefig("whf", format="png", dpi=1000)
    plt.show()


    # Wall heat flux = f(thickness)
    whf = PicklePLT()
    fig, axes = whf.load_pickle(path=paf + "post_traitement/images/Qwall_thickness.pickle")

    plt.close()
    plt.clf()

    fig2 = plt.figure()
    # then copy the relevant data from the dummy to the ax
    whf.move_axes(axes[1], fig2, subplot_spec=(111))
    whf.move_axes(axes[3], fig2, subplot_spec=(111))
    ax1 = fig2.axes[0]
    ax1.set_xlim(0.5,0.9)
    savefig("WHF_thickness", format="png")

    plt.show()


    # Interface flux
    # ---- Gas flux
    gf = PicklePLT()
    fig, axes = gf.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")
    axes[0].set_xlim(0,180)
    axes[0].set_ylim(-50000,200000)
    axes[0].legend(loc="lower left")
    savefig("GF", format="png", dpi=1000)
    plt.show()

    # ---- liquid flux
    gf = PicklePLT()
    fig, axes = gf.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")
    axes[0].legend(loc="lower left")
    axes[0].set_xlim(0, 180)
    axes[0].set_ylim(-500, 500)
    savefig("LF", format="png", dpi=1000)
    plt.show()

    # --- evap flux
    evap_flux = PicklePLT()
    fig, axes = evap_flux.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")
    axes[0].legend(loc="lower left")
    axes[0].set_xlim(0, 180)
    axes[0].set_ylim(-40000, 100000)
    savefig("evap_flux", format="png", dpi=1000)
    plt.show()
#run()

def run2():
    paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
    configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/graph_presentation")
    import os
    try:
        os.mkdir(paf + "post_traitement/graph_presentation")
    except:
        pass

    # Thickness
    thickness = PicklePLT()
    fig, axes = thickness.load_pickle(path=paf + "post_traitement/images/e_film.pickle")
    axes[0].set_ylim(0, 14)
    savefig("e_film", format="png", dpi=1000)
    plt.show()

    # Wall heat flux =
    whf = PicklePLT()
    fig, axes = whf.load_pickle(path=paf + "post_traitement/images/heat_flux.pickle")
    whf.move_annotation(label = '',x= 45)
    axes[0].legend(loc="lower left")
    savefig("whf", format="png", dpi=1000)
    plt.show()


    # Wall heat flux = f(thickness)
    whf = PicklePLT()
    fig, axes = whf.load_pickle(path=paf + "post_traitement/images/Qwall_thickness.pickle")

    plt.close()
    plt.clf()

    fig2 = plt.figure()
    # then copy the relevant data from the dummy to the ax
    whf.move_axes(axes[1], fig2, subplot_spec=(111))
    whf.move_axes(axes[3], fig2, subplot_spec=(111))
    ax1 = fig2.axes[0]
    ax1.set_xlim(0,1)
    savefig("WHF_thickness", format="png")

    plt.show()


    # Interface flux
    # ---- Gas flux
    gf = PicklePLT()
    fig, axes = gf.load_pickle(path=paf + "post_traitement/images/gas_flux.pickle")
    axes[0].set_xlim(0,180)
    #axes[0].set_ylim(-50000,200000)
    axes[0].legend(loc="lower left")
    savefig("GF", format="png", dpi=1000)
    plt.show()

    # ---- liquid flux
    gf = PicklePLT()
    fig, axes = gf.load_pickle(path=paf + "post_traitement/images/liquid_flux.pickle")
    axes[0].legend(loc="lower left")
    axes[0].set_xlim(0, 180)
    #axes[0].set_ylim(-500, 500)
    savefig("LF", format="png", dpi=1000)
    plt.show()

    # --- evap flux
    evap_flux = PicklePLT()
    fig, axes = evap_flux.load_pickle(path=paf + "post_traitement/images/evap_flux.pickle")
    axes[0].legend(loc="lower left")
    axes[0].set_xlim(0, 180)
    #axes[0].set_ylim(-40000, 100000)
    savefig("evap_flux", format="png", dpi=1000)
    plt.show()

run2()
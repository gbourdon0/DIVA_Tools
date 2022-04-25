# Build an image with the geometry properties
# for this, need the first plot files
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from modules.data_reader.plt_obj import plt_obj as plt_object
from modules.global_variable.default_param import default_plot_param
import modules.global_variable.global_variable as gv
import matplotlib
from matplotlib.offsetbox import AnchoredText
import matplotlib.patches as mpatches
import modules.diva_input as DIVA


def build_image_2D_axi(paf, phi_to_plot=[]):
    # init
    tecplot = plt_object(paf + "/animation_files/anim001.plt")
    matplotlib.style.use("seaborn")
    extent = [min(tecplot["R"]), max(tecplot["R"]), min(tecplot["Z"]), max(tecplot["Z"])]
    fig, ax = plt.subplots()
    # plot phi
    k = 0
    color_set = ['k', 'tab:gray', 'tab:blue']
    labels = []
    for phi_name in phi_to_plot:
        phi_plot = tecplot[phi_name].reshape(tecplot.mesh_dim[1], tecplot.mesh_dim[0])
        c = plt.contour(phi_plot, levels=[0], colors=color_set[k], linestyles="-",
                        linewidths=default_plot_param["linewidths"],
                        zorder=default_plot_param["zorder"], extent=extent)
        labels.append(mpatches.Patch(color=color_set[k], label=phi_name))
        k += 1

    plt.legend(handles=labels)
    # Annontate boundary
    bbox = dict(boxstyle="round", fc="1")
    arrowprops = dict(arrowstyle="->")

    # Sur abscisse:

    # X1
    if gv.DIVA_input.TSC.coord_system == "Axisymetrical":
        text = "Boundary condition X1 : Axisymetric condition"
    else:

        text = "Boundary condition X1 : \n" + gv.DIVA_input.BC.get_X1_BC(rtype=str) + "\n" + gv.DIVA_input.TBC.get_X1_BC(
            rtype=str)
        if gv.DIVA_input.NS.mass_frac == "Mass fraction":
            text += "\n" + gv.DIVA_input.MFBC.get_X1_BC(rtype=str)
    at = AnchoredText(text, frameon=True, bbox_to_anchor=(1, .8), loc='center left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:purple"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    at = AnchoredText("X1", frameon=True, bbox_to_anchor=(0, .5), loc='center left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:purple"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    plt.vlines(extent[0], extent[2], extent[3], colors="tab:purple", linewidths=default_plot_param["linewidths"])

    # XN
    text = "Boundary condition XN : \n" + gv.DIVA_input.BC.get_XN_BC(
        rtype=str) + "\n" + gv.DIVA_input.TBC.get_XN_BC(
        rtype=str)
    if gv.DIVA_input.NS.mass_frac == "Mass fraction":
        text +="\n" + gv.DIVA_input.MFBC.get_XN_BC(rtype=str)
    at = AnchoredText(text, frameon=True, bbox_to_anchor=(1., 0.6), loc='center left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:red"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    at = AnchoredText("XN", frameon=True, bbox_to_anchor=(1, .5), loc='center right', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:red"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    plt.vlines(extent[1], extent[2], extent[3], colors="tab:red", linewidths=default_plot_param["linewidths"])

    # Sur ordonnee
    # Y1
    text = "Boundary condition Y1 : \n" + gv.DIVA_input.BC.get_Y1_BC(
        rtype=str) + "\n" + gv.DIVA_input.TBC.get_Y1_BC(
        rtype=str)
    if gv.DIVA_input.NS.mass_frac == "Mass fraction":
        text +="\n" + gv.DIVA_input.MFBC.get_Y1_BC(rtype=str)
    at = AnchoredText(text, frameon=True, bbox_to_anchor=(1., .4), loc='center left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:blue"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    at = AnchoredText("Y1", frameon=True, bbox_to_anchor=(0.5, 0.0), loc='lower left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:blue"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    plt.hlines(extent[2], extent[0], extent[1], colors="tab:blue", linewidths=default_plot_param["linewidths"])

    # YN
    text = "Boundary condition YN : \n" + gv.DIVA_input.BC.get_YN_BC(
        rtype=str) + "\n" + gv.DIVA_input.TBC.get_YN_BC(
        rtype=str)
    if gv.DIVA_input.NS.mass_frac == "Mass fraction":
        text +="\n" + gv.DIVA_input.MFBC.get_YN_BC(rtype=str)
    at = AnchoredText(text, frameon=True, bbox_to_anchor=(1., 0.2), loc='center left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:brown"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    at = AnchoredText("YN", frameon=True, bbox_to_anchor=(0.5, 1), loc='lower left', bbox_transform=ax.transAxes,
                      prop=dict(color="tab:brown"))
    at.patch.set_boxstyle("round,pad = 0, rounding_size = 0.2")
    ax.add_artist(at)
    plt.hlines(extent[3], extent[0], extent[1], colors="tab:brown", linewidths=default_plot_param["linewidths"])

    # toplot = data_reader["Temperature"].reshape(data_reader.mesh_dim[1],data_reader.mesh_dim[0])
    # plt.imshow(toplot, extent = [min(data_reader["R"]), max(data_reader["R"]),min(data_reader["Z"]),
    # max(data_reader["Z"])],origin ="lower" )

    plt.ylabel("Z [m]")
    plt.xlabel("R [m]")
    plt.axis('equal')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == "__main__":
    paf = "/work/gbourdon/02_benchmark_FC72/13_0/run"
    gv.DIVA_input = DIVA.diva_input()
    gv.DIVA_input.load(paf)
    build_image_2D_axi(paf = "/work/gbourdon/02_benchmark_FC72/13_0/", phi_to_plot=["Phi_solid", "Phi"])


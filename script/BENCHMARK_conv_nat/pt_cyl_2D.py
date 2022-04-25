"""
post_process function for the 2D axi post processing with IMB and thermal computation.
All post-treatment are defined as function, then if you want to do only some of them go to the end
(# Computation of the post treatment).
WARNING : if you don't do all the post-treatment, some of them might not work.
"""

import numpy as np
import pandas as pd
import os
import modules.post_proc_2D as pt
import modules.diva_input as DIVA_in
from modules.data_reader.Tecplot import Tecplot
import matplotlib.pyplot as plt


def pt_sphere(paf, plt_file, debug=False):
    # Import input
    DIVA_input = DIVA_in.diva_input()
    DIVA_input.load(paf + "/run")

    # Import plt files anim002.plt../animation_files/
    DIVA_plt = Tecplot()
    DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)

    # Create pre_output dataset
    # these two DataSet will be joined for the 1D data
    wall_1D = pd.DataFrame()
    interface_1D = pd.DataFrame()

    # 2D output dataset
    p_spectral = pd.DataFrame()

    # ******************************************************************************************************************
    #                                           HEAT FLUX
    # ******************************************************************************************************************
    def general_heat_flux():
        print("Compute General Heat Flux")
        pt.compute_gradient(DIVA_plt, frame=1, var_name="Temperature")
        pt.heat_flux(DIVA_plt, DIVA_input, frame=1, phi_sol_name="phi_solid")

        if debug:
            DIVA_plt.plot(flood = "Heat Flux", lines=["phi_solid"])
    # Compute Wall Heat Flux

    def wall_heat_flux():
        print("Compute Wall Heat Flux")
        pt.phi_normal(DIVA_plt, frame=1, phi_name="phi_solid")

        pt.compute_gradient(DIVA_plt, frame=1, var_name="Tghost_immersed_sol")

        pt.wall_heat_flux(DIVA_plt, DIVA_input, frame=1, phi_sol_name="phi_solid", phi_liq_name="Phi")
        wall_1D["theta_wall"], wall_1D["FLUX_wall"] = pt.angular_wall_heat_flux(DIVA_plt, frame=1,
                                                                                   phi_sol_name="phi_solid")

        if debug:
            print(wall_1D.columns)
            plt.plot(wall_1D["theta_wall"], -wall_1D["FLUX_wall"])
            plt.title("Wall heat Flux")
            plt.xlabel("Theta (deg)")
            plt.ylabel("Flux (W/m2)")
            plt.show()

    # Compute Interface Heat Flux

    # ******************************************************************************************************************
    #                                           Nu/h
    # ******************************************************************************************************************
    # coefficient d'echange - Solide/Vapeur
    def Nu_wg():
        print("Compute local wall Nusselt")
        DT = (DIVA_input.IC.T_immersed - DIVA_input.TBC.BCX1_dir)
        h_wg = wall_1D["FLUX_wall"] / DT
        wall_1D["h_ws"] = h_wg


    # ******************************************************************************************************************
    #                                           Pressure
    # ******************************************************************************************************************

    # ******************************************************************************************************************
    #                                           Velocity
    # ******************************************************************************************************************
    def polar_velocity():
        print("Compute projection of velocity in polar base")
        pt.polar_velocity(DIVA_plt, frame=1, phi_sol_name="phi_solid")



    # ******************************************************************************************************************
    #                                           Coordinates
    # ******************************************************************************************************************
    def polar_coordinates():
        print("Compute polar coordinates")
        pt.polar_coordinates(DIVA_plt, frame=1)

    # Write post-traitement
    try:
        os.mkdir(paf + "/post_traitement")
    except:
        pass

    try:
        os.mkdir(paf + "/post_traitement/data2D")
    except:
        pass
    try:
        os.mkdir(paf + "/post_traitement/data1D")
    except:
        pass
    try:
        os.mkdir(paf + "/post_traitement/data1D/wall")
    except:
        pass

    try:
        os.mkdir(paf + "/post_traitement/data1D/interface")
    except:
        pass

    # Computation of the post treatment

    general_heat_flux()
    wall_heat_flux()
    Nu_wg()
    # grad_p_spectral()

    #Polar conversion
    polar_coordinates()
    polar_velocity()




    name = plt_file.replace("anim", "").replace(".plt", "") + ".pickle"
    DIVA_plt.write_pickle(filename=paf + "/post_traitement/data2D/" + name)
    interface_1D.to_pickle(paf + "/post_traitement/data1D/interface/interface_" + name)
    wall_1D.to_pickle(paf + "/post_traitement/data1D/wall/wall_" + name)
    # p_spectral.to_pickle(paf + "/post_traitement/data1D/wall/wall_" + name)


if __name__ == "__main__":

    paf = "/home/gbourdon/03_DIVA_dev/000_BENCHMARK/05_conv_nat_benchmark"
    # paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
    # paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
    plt_file = "anim018.plt"
    DIVA_plt = Tecplot()
    #DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)
    #fig, ax = DIVA_plt.plot(1, flood="Temperature", lines=["phi_solid"],show = False)
    plt.show()
    pt_sphere(paf=paf, plt_file=plt_file, debug=True)

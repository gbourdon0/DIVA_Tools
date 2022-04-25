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
import time
t = time.time()
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
    gradP_1D = pd.DataFrame()
    # 2D output dataset
    p_spectral = pd.DataFrame()

    # Compute general Heat Flux

    def general_heat_flux():
        print("Compute General Heat Flux")
        pt.compute_gradient(DIVA_plt, frame=1, var_name="Temperature")
        pt.heat_flux(DIVA_plt, DIVA_input, frame=1, phi_sol_name="Phi_solid", phi_liq_name="Phi")
        if debug:
            DIVA_plt.plot(flood="Heat Flux",lines = ["Phi_solid"])

    # ******************************************************************************************************************
    #                                           HEAT FLUX
    # ******************************************************************************************************************

    # Compute Wall Heat Flux
    def wall_heat_flux():
        print("Compute Wall Heat Flux")
        pt.phi_normal(DIVA_plt, frame=1, phi_name="Phi_solid")
        pt.compute_gradient(DIVA_plt, frame=1, var_name="Tghost_immersed_sol")
        pt.wall_heat_flux(DIVA_plt, DIVA_input, frame=1, phi_sol_name="Phi_solid", phi_liq_name="Phi")
        wall_1D["theta_wall"], wall_1D["FLUX_wall"] = pt.angular_wall_heat_flux(DIVA_plt, frame=1,
                                                                                phi_sol_name="Phi_solid")

        if debug:
            # DIVA_plt.plot(flood="Wall Heat Flux_field", vector=["Phi_solid_nx", "Phi_solid_ny"], vscale=1e4,
            #                 zoom=[(0, 0.01), [-.01, .01]], lines = ["Phi_solid"])

            plt.plot(wall_1D["theta_wall"], wall_1D["FLUX_wall"])
            plt.title("Wall heat Flux")
            plt.xlabel("Theta (deg)")
            plt.ylabel("Flux (W/m2)")
            plt.show()




    # Compute Interface Heat Flux

    # Flux with fluid extention
    def interface_liq_flux():
        print("Compute Interface Fluid Flux")
        pt.phi_normal(DIVA_plt, frame=1, phi_name="Phi")
        pt.compute_gradient(DIVA_plt, frame=1, var_name="T_liq")
        pt.interface_liq_heat_flux(DIVA_plt, DIVA_input, frame=1, phi_liq_name="Phi")

        interface_1D["theta_interface"], interface_1D["FLUX_liq"] = pt.angular_interface_liq_heat_flux(DIVA_plt,
                                                                                                       frame=1,
                                                                                                       phi_liq_name="Phi",phi_sol_name="Phi_solid")

        if debug:
            # DIVA_plt.plot(flood="Wall Heat Flux_field", vector=["Phi_nx", "Phi_ny"], vscale=1e4,
            #                                zoom=[(0, 0.01), [-.01, .01]], lines = ["Phi"])

            plt.title("liq. heat Flux")
            plt.xlabel("Theta (deg)")
            plt.ylabel("Flux (W/m2)")
            plt.scatter(interface_1D["theta_interface"], interface_1D["FLUX_liq"])
            plt.show()

    # Flux with gas extension
    def interface_gas_flux():
        print("Compute Interface Gas Flux")
        # Le prolongement de la temperature peut diverger tres loin de l'interface, je limite donc la temperature pour
        # ne pas avoir d'erreur numerique sur des nombres infinis plus loin
        DIVA_plt.limiter(frame=1, var_name="T_gas", mini=0, maxi=1e5)
        pt.compute_gradient(DIVA_plt, frame=1, var_name="T_gas")
        pt.interface_gas_heat_flux(DIVA_plt, DIVA_input, frame=1, phi_liq_name="Phi")
        # angle,test = pt.interface_gas_heat_flux2(DIVA_plt, DIVA_input, frame=1, phi_liq_name="Phi")
        pt.interface_gas_heat_flux(DIVA_plt, DIVA_input, frame=1, phi_liq_name="Phi")
        interface_1D["theta_interface"], interface_1D["FLUX_gas"] = pt.angular_interface_gas_heat_flux(DIVA_plt,
                                                                                                       frame=1,
                                                                                                       phi_liq_name="Phi",
                                                                                                       phi_sol_name="Phi_solid")
        if debug:
            plt.title("Gas. heat Flux")
            plt.xlabel("Theta (deg)")
            plt.ylabel("Flux (W/m2)")
            plt.plot(interface_1D["theta_interface"], interface_1D["FLUX_gas"])
            plt.show()

    # Evaporation flow rate
    def interface_evap_flux():
        print("Compute evaporation Flux")
        DIVA_plt[1]["Evaporation flux"] = DIVA_plt[1]["Interface Gas Heat Flux_field"] - DIVA_plt[1][
            "Interface Liq Heat Flux_field"]
        interface_1D["FLUX_evap"] = np.array(interface_1D["FLUX_gas"] - interface_1D["FLUX_liq"])
        if debug:
            plt.plot(interface_1D["theta_interface"], interface_1D["FLUX_evap"])
            plt.show()

    # ******************************************************************************************************************
    #                                          FILM GEOMETRY
    # ******************************************************************************************************************
    # Epaisseur du film
    def film_thickness():
        print("Compute film thickness")
        xx, yy = DIVA_plt.get_film_interface(frame=1, phi_liq_name="Phi", phi_sol_name="Phi_solid", method = 2)

        #Reducing the data to speed up the interpolation
        df_reduce = DIVA_plt[1].data
        x_min, x_max, y_min, y_max = min(xx), max(xx), min(yy), max(yy)
        step = max(np.sqrt(DIVA_plt.dx ** 2 + DIVA_plt.dy ** 2))  # To get enough cells to perform interpolation
        df_reduce = df_reduce.loc[
            (df_reduce[DIVA_plt.x_label] >= x_min - step) & (df_reduce[DIVA_plt.x_label] <= x_max + step)
            & (df_reduce[DIVA_plt.y_label] >= y_min - step) & (df_reduce[DIVA_plt.y_label] <= y_max) - step]
        x, y = df_reduce[DIVA_plt.x_label], df_reduce[DIVA_plt.y_label]

        from modules.post_proc_2D.interp2D import interp2D
        interface_1D["Film thickness"] = abs(
            interp2D(np.array(df_reduce["Phi_solid"]), x, y, xx, yy, resolve_nan=True,
                     kind='linear'))[2:-2]
        if debug:
            plt.plot(interface_1D["theta_interface"], interface_1D["Film thickness"])
            plt.show()

    # ******************************************************************************************************************
    #                                           Nu and h
    # ******************************************************************************************************************
    # coefficient d'echange - Solide/Vapeur
    def Nu_wg():
        print("Compute local wall Nusselt")
        DT_sup = (DIVA_input.IC.T_immersed - DIVA_input.TP.t_sat)
        h_wg = wall_1D["FLUX_wall"] / DT_sup
        wall_1D["h_ws"] = h_wg

    # coefficient d'echange - Gaz
    def Nu_gl():
        print("Compute local gas Nusselts")
        DT_sub = (DIVA_input.IC.DT_sub)
        h_gl = interface_1D["FLUX_gas"] / DT_sub
        interface_1D["h_gl"] = h_gl

    # coefficient d'echange - Liquide
    def Nu_lg():
        print("Compute local liquid Nusselts")
        DT_sub = (DIVA_input.IC.DT_sub)
        h_fg = interface_1D["FLUX_liq"] / DT_sub
        interface_1D["h_fg"] = h_fg

    # ******************************************************************************************************************
    #                                           Pressure
    # ******************************************************************************************************************

    def grad_P():
        print("Compute pressure gradient")
        pt.compute_gradient(DIVA_plt, frame=1, var_name="Pressure")

    def gradP_avg():
        print("Compute the avg value of pressure gradient according radial coordinates")
        theta = np.arange(3, 110, 1)
        gradP_1D["mean_radial_gradP"], gradP_1D["std_radial_gradP"] = pt.gradP_film(theta, 1, DIVA_plt)
        gradP_1D["Theta"] = theta

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

    try:
        os.mkdir(paf + "/post_traitement/data1D/gradP")
    except:
        pass

    # ******************************************************************************************************************
    #                                           Choose what postproc you want
    # ******************************************************************************************************************
    # Computation of the post treatment
    #coordinates
    polar_coordinates()
    #heat flux
    general_heat_flux()
    wall_heat_flux()
    interface_liq_flux()
    interface_gas_flux()
    interface_evap_flux()
    #film tchikness
    film_thickness()
    #Nusselt
    Nu_wg()
    Nu_gl()
    Nu_lg()
    #Pressure
    grad_P()
    try:
        gradP_avg()
    except:
        print("WARNING : something went wrong with gradient pressure analysis from "+paf)


    # ******************************************************************************************************************
    #                                           Saving data
    # ******************************************************************************************************************

    ''' name = plt_file.replace("anim", "").replace(".plt", "") + ".pickle"
    DIVA_plt.write_pickle(paf + "/post_traitement/data2D/" + name)
    interface_1D.to_pickle(paf + "/post_traitement/data1D/interface/interface_" + name)
    wall_1D.to_pickle(paf + "/post_traitement/data1D/wall/wall_" + name)
    gradP_1D.to_pickle(paf + "/post_traitement/data1D/gradP/gradP_" + name)'''
    # p_spectral.to_pickle(paf + "/post_traitement/data1D/wall/wall_" + name)


if __name__ == "__main__":
    t = time.time()
    paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
    # paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
    paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
    plt_file = "anim160.plt"
    DIVA_plt = Tecplot()
    DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)
    pt_sphere(paf, plt_file, debug=False)
    print(time.time()-t)
    # pt_sphere(paf=paf, plt_file="anim147.plt", debug=True)


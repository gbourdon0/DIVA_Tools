import numpy as np


def old_heat_flux(Tecplot_obj, Diva_input_obj, frame, phi_sol_name, phi_liq_name = None):
    import modules.global_variable.global_variable as gv
    '''
    :param Tecplot_obj: 
    :param phi_nx: x component of normal vector of phi_solid 
    :param phi_ny: y component of normal vector of phi_solid 
    :return: Compute Heat Flux but not at interfaces
    '''
    # Variable reshapping
    if phi_liq_name != None:
        phi_liq = Tecplot_obj[frame][phi_liq_name].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    phi_sol = Tecplot_obj[frame][phi_sol_name].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    gradT_x = Tecplot_obj[frame]["\/Temperature_x"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    gradT_y = Tecplot_obj[frame]["\/Temperature_y"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])

    flux = []
    for i in range(Tecplot_obj[1].mesh_dim[0]):
        for j in range(Tecplot_obj[1].mesh_dim[1]):

            if phi_sol[i][j] < 0:
                if phi_liq_name != None: #if we have two phase flow
                    if phi_liq[i][j] > 0:
                        kappa = Diva_input_obj.TP.kth_liq
                    else:
                        kappa = Diva_input_obj.TP.kth_vap
                else: #monophasic
                    kappa=Diva_input_obj.TP.kth_vap
                flux.append(kappa * (gradT_x[i][j] ** 2 + gradT_y[i][j] ** 2) ** .5)
            else:
                flux.append(np.nan)
    Tecplot_obj[1]["Heat Flux"] = flux


def heat_flux(Tecplot_obj, Diva_input_obj, frame, phi_sol_name, phi_liq_name = None):

    '''
    :param Tecplot_obj: 
    :param phi_nx: x component of normal vector of phi_solid 
    :param phi_ny: y component of normal vector of phi_solid 
    :return: Compute Heat Flux but not at interfaces
    '''
    # Variable reshapping
    if phi_liq_name != None:
        phi_liq = Tecplot_obj[frame][phi_liq_name].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    gradT_x = Tecplot_obj[frame]["\/Temperature_x"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    gradT_y = Tecplot_obj[frame]["\/Temperature_y"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])

    kappa = np.zeros(gradT_x.shape)

    kappa[phi_liq>0] = Diva_input_obj.TP.kth_liq
    kappa[phi_liq<0] = Diva_input_obj.TP.kth_vap

    flux = kappa*np.sqrt(gradT_x**2+gradT_y**2)
    flux = flux.reshape(flux.shape[0]*flux.shape[1])
    Tecplot_obj[1]["Heat Flux"] = flux

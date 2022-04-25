import numpy as np


def interface_gas_heat_flux(Tecplot_obj, Diva_input_obj, frame, phi_liq_name):
    """
    :param phi_liq_name: phi name
    :param frame: frame number of the Tecplot obj
    :param Diva_input_obj: Diva_input_obj, as defined in diva_input
    :param Tecplot_obj: Tectplot_obj as defined in data_reader/Tecplot
    :return: Heat flux along the interface considering the interface to be in the center of the cell where phi near 0 to the cell
    """
    # Variable reshapping
    phi_nx = Tecplot_obj.get_grid_data(frame=frame, var_name=phi_liq_name + "_nx")
    phi_ny = Tecplot_obj.get_grid_data(frame=frame, var_name=phi_liq_name + "_ny")

    gradT_x = Tecplot_obj.get_grid_data(frame=frame, var_name="\/T_gas_x")
    gradT_y = Tecplot_obj.get_grid_data(frame=frame, var_name="\/T_gas_y")

    kappa = np.ones(gradT_x.shape) * Diva_input_obj.TP.kth_vap

    flux = -kappa * (gradT_x * phi_nx + gradT_y * phi_ny)
    flux = flux.reshape(flux.size)
    Tecplot_obj[frame]["Interface Gas Heat Flux_field"] = flux
    return None


def old_interface_gas_heat_flux(Tecplot_obj, Diva_input_obj, frame, phi_liq_name):
    """
    :param Diva_input_obj: Diva input object as defined in diva_input
    :param frame: frame number of the Tecplot_obj
    :param phi_liq_name: phi name in the .plt file (should be phi)
    :param Tecplot_obj: Tecplot_obj as defined in data_reader/Tecplot
    :return: Heat flux along the intefrace considering the interface to be in the center of the cell where phi near 0 to the cell
    """
    # Variable reshapping
    phi_nx = Tecplot_obj[frame][phi_liq_name + "_nx"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    phi_ny = Tecplot_obj[frame][phi_liq_name + "_ny"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    gradT_x = Tecplot_obj[frame]["\/T_gas_x"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    gradT_y = Tecplot_obj[frame]["\/T_gas_y"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    flux = []
    for i in range(Tecplot_obj[1].mesh_dim[0]):
        for j in range(Tecplot_obj[1].mesh_dim[1]):
            kappa = Diva_input_obj.TP.kth_vap
            flux.append(-kappa * ((phi_nx[i][j]) * gradT_x[i][j] + phi_ny[i][j] * gradT_y[i][j]))
    Tecplot_obj[frame]["Interface Gas Heat Flux_field"] = flux
    return None


def angle_of_vectors(a: list, b: list) -> float:
    """
    Compute angle between vector a and b for 2D vector
    :param a: should be a size 2 list
    :param b: should be a size 2 list
    :return: angle in degree
    """
    import numpy as np
    import numpy.linalg as LA

    inner = np.inner(a, b)
    norms = LA.norm(a) * LA.norm(b)
    if norms == 0.0:
        return None
    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    deg = np.rad2deg(rad)
    return deg


def old_angular_interface_gas_heat_flux(Tecplot_obj, frame, phi_liq_name, phi_sol_name):
    """
    Compute the angular heat flux from gas to liquid (without the evaporation rate)
    :param Tecplot_obj: tecplot_obj as defined in data_reader/Tecplot
    :param frame: frame number (or .plt number) for the Tecplot_obj
    :param phi_liq_name: phi name should be phi
    :return:angle list and associated heat flux
    """
    xx, yy = Tecplot_obj.get_film_interface(frame=frame, phi_liq_name=phi_liq_name,phi_sol_name =phi_sol_name)
    x, y = Tecplot_obj[frame][Tecplot_obj.x_label], Tecplot_obj[frame][Tecplot_obj.y_label]
    from scipy import interpolate
    points = np.transpose(np.vstack((x, y)))
    '''FLUX = np.array(
        interpolate.griddata(points, Tecplot_obj[frame]["Interface Gas Heat Flux_field"], (xx, yy), method='cubic',
                             rescale=True))'''
    # To not bug the interp, sort of remove nan from the list
    grid_x, grid_y = xx,yy
    points = np.array([x,y])
    values = Tecplot_obj[frame]["Interface Gas Heat Flux_field"]

    values[0] = np.nan  # now add a single nan value to the array

    # Find all the indexes where there is no nan neither in values nor in points.
    nonanindex = np.invert(np.isnan(points[0, :])) * np.invert(np.isnan(points[1,:])) * np.invert(np.isnan(values))

    # Remove the nan using fancy indexing. griddata can now properly interpolate. The result will have nan only on
    # the edges of the array
    from scipy.interpolate import griddata
    FLUX = griddata(np.stack((points[0,nonanindex], points[1,nonanindex]), axis=1), values[nonanindex],
                      (grid_x, grid_y), method='cubic')

    theta2 = np.array([angle_of_vectors([0, -1], [xx[i], yy[i]]) for i in range(len(xx))])
    return theta2[2:-2], FLUX[2:-2]  # To remove first and last value of angle which are inconsistent due to derivative

def angular_interface_gas_heat_flux(Tecplot_obj, frame, phi_liq_name,phi_sol_name):
    """
    Compute the angular heat flux from gas to liquid (without the evaporation rate)
    :param phi_sol_name: name of the phi function for the IMB
    :param Tecplot_obj: tecplot_obj as defined in data_reader/Tecplot
    :param frame: frame number (or .plt number) for the Tecplot_obj
    :return:angle list and associated heat flux
    """
    xx, yy = Tecplot_obj.get_film_interface(frame=frame, phi_liq_name=phi_liq_name,
                                                              phi_sol_name= phi_sol_name, method = 2)

    from modules.post_proc_2D.interp2D import interp2D

    # Reducing the data to speed up the interpolation
    df_reduce = Tecplot_obj[frame].data
    x_min,x_max,y_min,y_max = min(xx),max(xx),min(yy),max(yy)
    step = max(np.sqrt(Tecplot_obj.dx**2+Tecplot_obj.dy**2)) #To get enough cells to perform interpolation
    df_reduce = df_reduce.loc[(df_reduce[Tecplot_obj.x_label]>=x_min-step) & (df_reduce[Tecplot_obj.x_label]<=x_max+step)
     & (df_reduce[Tecplot_obj.y_label]>=y_min-step) & (df_reduce[Tecplot_obj.y_label]<=y_max)-step]
    x,y = df_reduce[Tecplot_obj.x_label],df_reduce[Tecplot_obj.y_label]

    #interpolating
    FLUX = interp2D(np.array(df_reduce["Interface Gas Heat Flux_field"]), x, y, xx, yy, resolve_nan = True,kind = 'linear')
    from modules.usefull_functions.base_change import cart2polar
    r, theta2 = cart2polar(xx,yy)
    theta2 +=90#to get 0° at the bottom

    return theta2[2:-2], FLUX[2:-2]  # To remove first and last value of angle which are inconsitent due to derivative

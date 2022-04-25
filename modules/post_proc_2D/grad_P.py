import numpy as np
import modules.post_proc_2D as pt


def rad_grad_p(Tecplot_obj, frame, phi_sol_name):
    """
    Compute the radial grad P with interpolating in the exact location of phi_sol = 0
    :param phi_sol_name: name of the phi function for the IMB
    :param frame: number of the frame for Tecplot_obj
    :param Diva_input_obj: Input Diva obj as defined in diva_input
    :param Tecplot_obj: Tecplot_obj as defined in data_reader/Tecplot
    :return: radial component of the pressure gradient
    """
    # Variable reshapping
    phi_nx = Tecplot_obj[frame][phi_sol_name + "_nx"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])
    phi_ny = Tecplot_obj[frame][phi_sol_name + "_ny"].reshape(Tecplot_obj[1].mesh_dim[0], Tecplot_obj[1].mesh_dim[1])

    gradT_x = Tecplot_obj[frame]["\/Pressure_x"].reshape(Tecplot_obj[1].mesh_dim[0],
                                                         Tecplot_obj[1].mesh_dim[1])
    gradT_y = Tecplot_obj[frame]["\/Pressure_y"].reshape(Tecplot_obj[1].mesh_dim[0],
                                                         Tecplot_obj[1].mesh_dim[1])
    rad_gradP = []
    theta_gradP = []
    def rot(x,y,theta):
        return x*np.cos(theta)-y*np.sin(theta),x*np.sin(theta)+y*np.cos(theta)
    for i in range(Tecplot_obj[1].mesh_dim[0]):
        for j in range(Tecplot_obj[1].mesh_dim[1]):
            rad_gradP.append(((phi_nx[i][j]) * gradT_x[i][j] + phi_ny[i][j] * gradT_y[i][j]))
            nx,ny = rot(phi_nx[i][j],phi_ny[i][j],theta = np.deg2rad(90))
            theta_gradP.append(float((nx * gradT_x[i][j] + ny * gradT_y[i][j])))

    Tecplot_obj[frame]["\/Pressure_r"] = rad_gradP
    Tecplot_obj[frame]["\/Pressure_theta"] = theta_gradP
    return None


def angle_of_vectors(a, b):
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


def angular_rad_grad_p(Tecplot_obj, frame, phi_sol_name):
    """
    Compute the angular distribution of the radial part of \/P
    :param phi_sol_name: name of the phi function for the IMB
    :param Tecplot_obj: tecplot_obj as defined in data_reader/Tecplot
    :param frame: frame number (or .plt number) for the Tecplot_obj
    :return:angle list and associated heat flux
    """
    xx, yy = Tecplot_obj.get_iso_value_2D(frame=1, var_name=phi_sol_name, iso_values=[0])
    x, y = Tecplot_obj[frame][Tecplot_obj.x_label], Tecplot_obj[frame][Tecplot_obj.y_label]
    ''' from scipy import interpolate
    points = np.transpose(np.vstack((x, y)))
       FLUX = np.array(interpolate.griddata(points, Tecplot_obj[frame]["Wall Heat Flux_field"], (xx, yy), method='cubic',
                                         rescale=True))
    '''
    # To not bug the interp, sort of remove nan from the list

    grid_x, grid_y = xx, yy
    points = np.array([x, y])
    values = Tecplot_obj[frame]["\/Pressure_r"]

    values[0] = np.nan  # now add a single nan value to the array

    # Find all the indexes where there is no nan neither in values nor in points.
    nonanindex = np.invert(np.isnan(points[0, :])) * np.invert(np.isnan(points[1, :])) * np.invert(np.isnan(values))

    # Remove the nan using fancy indexing. griddata can now properly interpolate. The result will have nan only on
    # the edges of the array
    from scipy.interpolate import griddata
    FLUX = griddata(np.stack((points[0, nonanindex], points[1, nonanindex]), axis=1), values[nonanindex],
                    (grid_x, grid_y), method='cubic')

    theta2 = np.array([angle_of_vectors([0, -1], [xx[i], yy[i]]) for i in range(len(xx))])
    return theta2[2:-2], FLUX[2:-2]  # To remove first and last value of angle which are inconsitent due to derivative


def rad_spectral_pressure(Tecplot_obj, frame, phi_sol_name, phi_liq_name):
    """
    Compute the spectral of the radial grad_p. The aim is to ploot \/P_r = f(Theta,e(Theta)
    :param Tecplot_obj: Tecplot_obj
    :param frame: frame number of tecplot obj
    :param phi_sol_name: phi solid name
    :param phi_liq_name: phi liquid name
    :return: theta (azimutal angle),e_film (film thickness at (x,y)), pressure the radial grad pressure
    """
    df = Tecplot_obj[frame].data
    df = df.loc[(df[phi_liq_name] < 0) & (df[phi_sol_name] < 0)]  # Take the film zone only

    xx, yy = np.array(df[Tecplot_obj.x_label]), np.array(df[Tecplot_obj.y_label])  # Where to interpolate
    x, y = np.array(Tecplot_obj[frame][Tecplot_obj.x_label]), np.array(Tecplot_obj[frame][Tecplot_obj.y_label])  # input grid
    pressure = pt.interp2D(np.array(Tecplot_obj[frame]["\/Pressure_r"]), x, y, xx, yy,resolve_nan = True)
    e_film = -pt.interp2D(np.array(Tecplot_obj[frame][phi_sol_name]), x, y, xx, yy, resolve_nan = True)
    theta = np.array([angle_of_vectors([0, -1], [xx[i], yy[i]]) for i in range(len(xx))])
    return theta, e_film, pressure


def rad_spectral_pressure2(Tecplot_obj, frame, phi_sol_name, phi_liq_name):
    """
    Compute the spectral of the radial grad_p. The aim is to ploot \/P_r = f(Theta,e(Theta)
    :param Tecplot_obj: Tecplot_obj
    :param frame: frame number of tecplot obj
    :param phi_sol_name: phi solid name
    :param phi_liq_name: phi liquid name
    :return: theta (azimutal angle),e_film (film thickness at (x,y)), pressure the radial grad pressure
    """
    df = Tecplot_obj[frame].data

    xx, yy = np.array(df[Tecplot_obj.x_label]), np.array(df[Tecplot_obj.y_label])  # Where to interpolate
    x, y = np.array(Tecplot_obj[frame][Tecplot_obj.x_label]), np.array(Tecplot_obj[frame][Tecplot_obj.y_label])  # input grid
    pressure = pt.interp2D(np.array(Tecplot_obj[frame]["\/Pressure_r"]), x, y, xx, yy,resolve_nan = True)
    e_film = -pt.interp2D(np.array(Tecplot_obj[frame][phi_sol_name]), x, y, xx, yy,resolve_nan = True)
    theta = np.array([angle_of_vectors([0, -1], [xx[i], yy[i]]) for i in range(len(xx))])
    return theta, e_film, pressure

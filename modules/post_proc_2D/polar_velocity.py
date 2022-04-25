import numpy as np


def polar_velocity(Tecplot_obj, frame):
    """
    Project the velocity on polar coordinates
    :param Tecplot_obj: A tectplot obj
    :param frame: frame number of tecplot obj
    :return: None
    """

    # Detect geometry type
    if Tecplot_obj.geom_type == "2D":
        u_name = "U"
        v_name = "V"
    elif Tecplot_obj.geom_type == "2D_axi":
        u_name = "U_r"
        v_name = "U_z"
    else:
        raise NotImplementedError(f"{Tecplot_obj.geom_type} geometry type is not implemented in this post porcessing")

    v_x = np.array(Tecplot_obj[frame][u_name])
    v_y = np.array(Tecplot_obj[frame][v_name])
    R = np.array(Tecplot_obj[frame]["R_polar"])
    Theta = np.array(Tecplot_obj[frame]["Theta_polar"])

    def rot(x, y, theta):
        return x * np.cos(theta) - y * np.sin(theta), x * np.sin(theta) + y * np.cos(theta)

    nx, ny = R*np.sin(np.deg2rad(Theta)), -R*np.cos(np.deg2rad(Theta))  # u_r vector
    norm = np.sqrt((nx**2+ny**2))
    norm[norm <= 0] = np.nan #if norm = 0, replace by nan to allow division
    nx,ny = nx/norm,ny/norm
    Tecplot_obj[frame]["er_x"] = nx
    Tecplot_obj[frame]["er_y"] = ny

    rad_v = (nx * v_x + ny * v_y)
    nx, ny = rot(nx, ny, theta=np.deg2rad(90))  # rotate 90 to get u_theta
    theta_v = (nx * v_x + ny * v_y)

    Tecplot_obj[frame]["etheta_x"] = nx
    Tecplot_obj[frame]["etheta_y"] = ny

    Tecplot_obj[frame]["U_polar_r"] = rad_v
    Tecplot_obj[frame]["U_polar_theta"] = theta_v


def polar_velocity_ghost_liq(Tecplot_obj, frame):
    """
    Project the velocity on polar coordinates
    :param Tecplot_obj: A tectplot obj
    :param frame: frame number of tecplot obj
    :return: None
    """

    v_x = np.array(Tecplot_obj[frame]["ughost_liq"])
    v_y = np.array(Tecplot_obj[frame]["vghost_liq"])
    R = np.array(Tecplot_obj[frame]["R_polar"])
    Theta = np.array(Tecplot_obj[frame]["Theta_polar"])

    def rot(x, y, theta):
        return x * np.cos(theta) - y * np.sin(theta), x * np.sin(theta) + y * np.cos(theta)

    nx, ny = R * np.sin(np.deg2rad(Theta)), -R * np.cos(np.rad2deg(Theta))  # u_r vector
    norm = (nx ** 2 + ny ** 2) ** .5
    try:
        nx, ny = nx / norm, ny / norm
    except:
        nx, ny = np.nan, np.nan

    rad_v = (nx * v_x + ny * v_y)
    nx, ny = rot(nx, ny, theta=np.deg2rad(90))  # rotate 90 to get u_theta
    theta_v = (nx * v_x + ny * v_y)


    Tecplot_obj[frame]["U_ghost_liq_polar_r"] = rad_v
    Tecplot_obj[frame]["U_ghost_liq_polar_theta"] = theta_v


def polar_velocity_ghost_gas(Tecplot_obj, frame, phi_sol_name):
    """
    Project the velocity on polar coordinates
    :param Tecplot_obj: A tectplot obj
    :param frame: frame number of tecplot obj
    :return: None
    """

    v_x = np.array(Tecplot_obj[frame]["ughost_gas"])
    v_y = np.array(Tecplot_obj[frame]["vghost_gas"])
    R = np.array(Tecplot_obj[frame]["R_polar"])
    Theta = np.array(Tecplot_obj[frame]["Theta_polar"])

    def rot(x, y, theta):
        return x * np.cos(theta) - y * np.sin(theta), x * np.sin(theta) + y * np.cos(theta)

    nx, ny = R * np.sin(np.deg2rad(Theta)), -R * np.cos(np.rad2deg(Theta))  # u_r vector
    norm = (nx ** 2 + ny ** 2) ** .5
    try:
        nx, ny = nx / norm, ny / norm
    except:
        nx, ny = np.nan, np.nan

    rad_v = (nx * v_x + ny * v_y)
    nx, ny = rot(nx, ny, theta=np.deg2rad(90))  # rotate 90 to get u_theta
    theta_v = (nx * v_x + ny * v_y)

    Tecplot_obj[frame]["U_ghost_gas_polar_r"] = rad_v
    Tecplot_obj[frame]["U_ghost_gas_polar_theta"] = theta_v

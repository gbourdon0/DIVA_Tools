import numpy as np


def polar_coordinates(Tecplot_obj, frame):
    """
    Compute the polar coordinates
    :param Tecplot_obj: A tectplot obj
    :param frame: frame number of tecplot obj
    :return: None
    """

    x = Tecplot_obj[frame][Tecplot_obj.x_label]
    y = Tecplot_obj[frame][Tecplot_obj.y_label]

    import copy
    is_x_negative = copy.deepcopy(x) #Pour avoir de 0 a 360 deg
    is_x_negative[x<0] = 1
    is_x_negative[x >= 0] = 0
    R = np.sqrt(x**2+y**2)
    Theta = np.arctan(y/x) + is_x_negative*np.pi


    Tecplot_obj[frame]["R_polar"] = R
    Tecplot_obj[frame]["Theta_polar"] = Theta
    Tecplot_obj[frame]["Theta_polar"] = np.rad2deg(
        Tecplot_obj[frame]["Theta_polar"] + np.pi / 2)  # Pour avoir de 0 deg en bas

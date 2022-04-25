import numpy as np
def cart2polar(x, y):
    """
    Transform a set of cartesienne 2D parameter into polar coordinate parameter
    :param x:
    :param y:
    :return:
    """
    import copy
    is_x_negative = copy.deepcopy(x)  # Pour avoir de 0 a 360 deg
    is_x_negative[x < 0] = 1
    is_x_negative[x >= 0] = 0
    R = np.sqrt(x ** 2 + y ** 2)
    Theta = np.arctan(y / x) + is_x_negative * np.pi

    return R, np.rad2deg(Theta)


def polar2cart(r, theta):
    """
    Transform a set of polar coordinate into 2D cartesienne coordinates
    :param r:
    :param theta:
    :return:
    """
    theta = theta
    x = r / np.sqrt((1 + np.tan(np.deg2rad(theta)) ** 2))
    y = x * np.tan(np.deg2rad(theta))
    return x, y
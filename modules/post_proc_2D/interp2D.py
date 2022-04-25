import numpy as np


def interp2D(value, x, y, xx, yy,resolve_nan = False,kind = 'cubic', fill_value = None):
    """
    Process interp2D
    :param value: konwn value of the field
    :param x: x list where values are defined
    :param y: y list where values are defined
    :param xx: x list where the value will be interpolated
    :param yy: y list where the value will be interpolated
    :return:
    """
    from scipy.interpolate import griddata
    import copy
    grid_x, grid_y = xx, yy
    points = np.array([x, y])
    values = np.array(value)

    if resolve_nan:
        values[0] = np.nan  # now add a single nan value to the array


        # Find all the indexes where there is no nan neither in values nor in points.

        nonanindex = np.invert(np.isnan(points[0, :])) * np.invert(np.isnan(points[1, :])) * np.invert(np.isnan(values))

        # Remove the nan using fancy indexing. griddata can now properly interpolate. The result will have nan only on
        # the edges of the array
        if fill_value == None: #allow extrapolation
            out = griddata(np.stack((points[0, nonanindex], points[1, nonanindex]), axis=1), values[nonanindex],
                           (grid_x, grid_y), method=kind)
        else:
            out = griddata(np.stack((points[0, nonanindex], points[1, nonanindex]), axis=1), values[nonanindex],
                           (grid_x, grid_y), method=kind, fill_value = fill_value)
    else:
        if fill_value == None:
            out = griddata((points[0], points[1]), values,
                           (grid_x, grid_y), method=kind)
        else:
            out = griddata((points[0], points[1]), values,
                           (grid_x, grid_y), method=kind, fill_value =fill_value)
    return out

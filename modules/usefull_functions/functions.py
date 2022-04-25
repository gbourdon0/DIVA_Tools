import numpy as np

def maximums(X, Y, max_number=1, get_idx = False):
    idx_list = []
    if max_number > len(Y):
        raise Exception(f"max_number cannot higher than the length of the input list; list length {len(Y)}")
    import copy
    L = copy.deepcopy(list(Y))
    XX = copy.deepcopy(list(X))
    YY = copy.deepcopy(list(Y))
    y_maximum = []
    x_maximum = []
    while len(y_maximum) < max_number:
        m = max(L)
        y_maximum.append(m)
        idx = YY.index(m)
        x_maximum.append(XX[idx])
        idx_list.append(idx)
        L.remove(m)
    x_maximum = list(reversed(x_maximum))
    y_maximum = list(reversed(y_maximum))
    idx_list= list(reversed(idx_list))
    if get_idx:
        return x_maximum, y_maximum, idx_list

    return x_maximum, y_maximum

def minimums(X, Y, max_number=1, get_idx = False):
    idx_list = []
    if max_number > len(Y):
        raise Exception(f"max_number cannot higher than the length of the input list; list length {len(Y)}")
    import copy
    L = copy.deepcopy(list(Y))
    XX = copy.deepcopy(list(X))
    YY = copy.deepcopy(list(Y))
    y_maximum = []
    x_maximum = []
    while len(y_maximum) < max_number:
        m = min(L)
        y_maximum.append(m)
        idx = YY.index(m)
        x_maximum.append(XX[idx])
        idx_list.append(idx)
        L.remove(m)
    x_maximum = list(reversed(x_maximum))
    y_maximum = list(reversed(y_maximum))
    idx_list= list(reversed(idx_list))
    if get_idx:
        return x_maximum, y_maximum, idx_list

    return x_maximum, y_maximum

def nearest_value(liste, look_for):
    """
    return nearest value and the idx on the liste
    :param liste: liste of values
    :param look_for: value you are looking for
    :return: nearest value, and index in the list
    """
    dif = np.absolute(liste - look_for)
    idx = dif.argmin()
    return liste[idx],idx
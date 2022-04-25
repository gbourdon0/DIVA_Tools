import numpy as np
from scipy.interpolate import interp1d


def convergence_1D(pickle_reader, x_name, y_name, x_list=[], idx_start_stat= None, t_start_time = None):
    """
    for all the time in pickle reader, compute the convergence of the given variable. From the index idx_start_stat,
    compute the mean and std of the variable. !!! utilise une interpolation CUBIC
    :param y_name: name of the y value in the pickle_reader
    :param x_name: name of the x value in de pickle_readed
    :param pickle_reader: a pickle_reader object
    :param x_list: the x list where the data will be evaluated. If not specified, the x_list of the pickle_reader
    :param idx_start_stat: start to process stat on the data (to compute mean and std). Should be once the data is 
    converged
    :return: convergence (for all time, give the convergence), mean and std
    """
    if idx_start_stat != None and t_start_time != None:
        raise Exception("You should choose either a idx start for the stat or a time, bu cannot be both of them.")
    if idx_start_stat == None and t_start_time == None:
        idx_start_stat = 0
    if t_start_time !=None:
        temp = np.abs(pickle_reader.time-t_start_time)
        idx_start_stat = temp.argmin()

    convergence = []  # check convergence
    if x_list == []:
        x_list = pickle_reader[x_name]
    stat = np.zeros((len(x_list), len(pickle_reader.key_list) - idx_start_stat))

    for i in range(0, len(pickle_reader.key_list)):
        df = pickle_reader[pickle_reader.key_list[i]].loc[pickle_reader[pickle_reader.key_list[i]][x_name] < x_list[-1]]

        f1 = interp1d(df[x_name], df[y_name],
                      kind='cubic', fill_value="extrapolate")
        if i < len(pickle_reader.key_list) - 1:
            df2 = pickle_reader[pickle_reader.key_list[i + 1]].loc[
                pickle_reader[pickle_reader.key_list[i + 1]][x_name] < x_list[-1]]
            f2 = interp1d(df2[x_name],
                          df2[y_name], kind='cubic', fill_value="extrapolate")
        try:
            diff = sum(abs(f1(x_list) - f2(x_list))) / sum(abs(f1(x_list)))
        except:
            diff = np.nan  # in case
        convergence.append(diff)
        if i >= idx_start_stat:
            stat[:,i - idx_start_stat] = f1(x_list)

    mean = np.mean(stat, axis=1)
    std = np.std(stat, axis=1)

    return convergence, mean, std, idx_start_stat

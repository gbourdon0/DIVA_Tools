from typing import List

import numpy as np
import pandas as pd


def read_dat(path):
    """
    :param path: path of the DIVA .dat file
    :return: as pandas DatFrame with the data on the .dat file
    """
    f = open(path)
    file = f.readlines()
    f.close()
    df = pd.DataFrame()
    header = file[1].replace(" ", "").replace("VARIABLES=", "").replace("\n", "").replace('"', '').split(",")
    temp = np.zeros((len(file) - 2, len(header),))  # -2, because data start on the 3rd line
    for i in range(2, len(file)):
        line: list[str] = file[i].replace("\n", "").split(" ")[1:]
        line = ' '.join(line).split()
        try:
            temp[i - 2, :] = np.array(line, dtype='float64')
        except:
            raise Exception(f'Cannot convert  line : "{line}", into a data structure. \n Reading file {path}')
    for col in range(len(header)):
        df[header[col]] = temp[:, col]

    df= df.sort_values('t(s)')
    return df

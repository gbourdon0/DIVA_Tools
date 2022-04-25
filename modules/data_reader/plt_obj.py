import pandas as pd
import numpy as np
from modules.data_reader import tecplotPltReader as tpr


class plt_obj:
    def __init__(self, filename: str) -> None:
        # Variables
        self.name: str = ''
        self.time: float = 0
        self.time_step: float = 0
        self.data: type(pd.DataFrame()) = pd.DataFrame()
        self.mesh_dim: tuple = (0, 0, 0)

        # Initialization function
        self.Reading_plt(filename)

    def Reading_plt(self, filename: str) -> None:
        """
        Load plt data into the class plt_obj
        :param filename: name of the plt file
        :return: None
        """
        self.name = filename.replace(".plt", "")
        print(f"Reading file : {filename}")

        file_to_read = open(filename, "rb")
        bytes_list = file_to_read.read()
        infos, read_binary = tpr.read_data(bytes_list, file_to_read)
        file_to_read.close()

        # Attributing info
        self.time = float(infos["Zones"][0]["ZoneName"].split(",")[1].split("=")[1])
        self.time_step = float(infos["Zones"][0]["ZoneName"].split(",")[0].split("=")[1])
        self.mesh_dim = (infos["Zones"][0]["Imax"], infos["Zones"][0]["Jmax"], infos["Zones"][0]["Kmax"])

        # Getting the data
        for var in infos["VarNames"]:
            self.data[var] = np.array(read_binary["Zones"][0][var])

    def __getitem__(self, name: str):
        return np.array(self.data[name])

    def __setitem__(self, key, value):
        self.data[key] = value



import pandas as pd
import os
import numpy as np


class PickleReader:
    def __init__(self):
        self.files = {}  # dictionary containing keys and pandas DataFrame
        self.key_list = []
        self.time = []

    # Load action
    def load_file(self, path):
        """
        load a .pickle file
        :param path: path for the file
        :return: None
        """
        name = ''
        try:
            name = path.split("/")[-1]
        except:
            name = path
        self.files[name] = pd.read_pickle(path)
        self.key_list.append(name)

    def load_folder(self, folder_path):
        """
        load all .pickle file in a fodler
        :param folder_path: folder path
        :return: None
        """
        files = os.listdir(folder_path)
        files.sort()
        for file in files:
            if ".pickle" in file:
                self.load_file(folder_path + "/" + file)
        print(f"pickle_reader : {len(self.files)} files founded !")
    def define_time(self, time):
        if len(time) != len(self.key_list):
            raise Exception(
                f"time argument should be the same length as key_list. Actually, {len(time)} and {len(self.key_list)}")
        else:
            self.time = time

    def get_header(self):
        key = list(self.files.keys())[0]
        return self.files[key].columns

    def get_file_time(self, look_time: float):
        """
        return the nearest frame for a given time
        :param look_time: time we are looking for
        :return: plt_obj with the nearest type from look_time
        """
        # Return the frame with the nearest time
        dif = np.absolute(np.array(self.time) - look_time)
        return self.files[self.key_list[dif.argmin()]]

    def time2plt(self, look_time):
        """
        return the plt position to the nearest given time
        :param look_time: time looking for
        :return:
        """
        dif = np.absolute(np.array(self.time - look_time))
        return dif.argmin()
    # Operator action

    def __getitem__(self, item):
        if type(item) == str:
            return self.files[item]
        elif type(item) == float:
            return self.get_file_time(item)
        else:
            raise Exception("item should be str (to specify  file name) or float (to get the nearest time file")

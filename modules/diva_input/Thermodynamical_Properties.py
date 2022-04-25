import modules.diva_input.dictionnary_diva as dico


class Thermodynamical_Properties:
    def __init__(self):
        # Liquide properties
        self.cp_liq = None
        self.kth_liq = None
        self.mol_mass_liq = None

        # gas properties
        self.cp_vap = None
        self.kth_vap = None
        self.mol_mass_vap = None

        # boiling properties
        self.hfg = None
        self.t_sat = None

        # external properties
        self.p0 = None
        self.mass_dif_coef = None

        # enthalpy diffusion
        self.enthalpy_diff_unable = None
        self.enthalpy1 = None
        self.enthalpy2 = None

    def read_file(self, path):
        """
        Load the input file data in the class
        :param path: path of the run folder of diva
        :return: None
        """
        f = open(path + "/Input_File_Thermodynamical_Properties", "r")
        files = f.readlines()
        f.close()
        files = iter(files)
        for lines in files:
            if "*LIQUID PHASE" in lines:
                next(files)
                self.cp_liq = self.get_value(next(files), 1, v_type=float)
                self.kth_liq = self.get_value(next(files), 1, v_type=float)
                self.mol_mass_liq = self.get_value(next(files), 1, v_type=float)
            if "*GAS PHASE" in lines:
                next(files)
                self.cp_vap = self.get_value(next(files), 1, v_type=float)
                self.kth_vap = self.get_value(next(files), 1, v_type=float)
                self.mol_mass_vap = self.get_value(next(files), 1, v_type=float)
            if "*INTERFACE PHYSICAL PROPERTIES" in lines:
                next(files)
                self.hfg = self.get_value(next(files), 1, v_type=float)
                self.t_sat = self.get_value(next(files), 1, v_type=float)
            if "*EXTERNAL PRESSURE" in lines:
                next(files)
                self.p0 = self.get_value(next(files), 1, v_type=float)
            if "*MASS DIFFUSION COEFFICIENT" in lines:
                next(files)
                self.mass_dif_coef = self.get_value(next(files), 1, v_type=float)
            if "*SPECIES ENTHALPY DIFFUSION" in lines:
                for i in range(4): next(files)
                self.enthalpy_diff_unable = dico.enthal_diff[self.get_value(next(files), 1, v_type=int)]
            if "*Enthalpy diffusion parameters" in lines:
                self.enthalpy1 = self.get_value(next(files), 1, v_type=float)
                self.enthalpy2 = self.get_value(next(files), 1, v_type=float)
        return None

    @staticmethod
    def get_value(line: str, nb_value: int, v_type=float):
        """
        :param line: line of the input file.
        :param nb_value: number of values that are in this line
        :param v_type: if the value if a float or an int
        :return: if one value : return the value
                 if nb_value>1 : return a nb_value list with the nb_value(s) inside
        """
        line = line.replace("\t", " ").split(" ")
        line = [item for item in line if item != '']  # remove empty elem
        out = []

        if nb_value == 1:
            value = line[0]
            if "d" in value:
                value = value.replace("d", "e")
            if v_type == float:
                value = float(value)
            if v_type == int:
                value = int(value)
            return value

        for i in range(nb_value):
            value = line[i]
            if "d" in value:
                value = value.replace("d", "e")
            if v_type == float:
                value = float(value)
            if v_type == int:
                value = int(value)
            out.append(value)
        return out

    @staticmethod
    def apply_dico(dico, key_list, rtype=tuple):
        """
        Apply a list of keys to a dictonnary
        :param key_list: list of keys
        :param dico: a dictionnary
        :param rtype: if rtype = tuple, return a tuple with the element corresponding to the key list. else return a list
        :return:
        """
        ''' Apply a dictionnary to a whole list'''
        # To apply a dictionnary to a whole list or tuple
        out_list = []
        for elem in key_list:
            out_list.append(dico[elem])
        if rtype == tuple:
            return tuple(out_list)
        return out_list

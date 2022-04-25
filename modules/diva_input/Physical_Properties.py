import modules.diva_input.dictionnary_diva as dico


class Physical_Properties:
    def __init__(self):
        self.rho_liq = None
        self.mu_liq = None
        self.rho_vap = None
        self.mu_vap = None
        self.sigma = None
        self.contact_angle = None
        self.g = (0, 0, 0)
        self.marangoni_type = None
        self.marangoni_surf_tens_grad = None
        self.marangoni_ref_T = None
        self.marangoni_ref_sigma_at_tref = None

        self.variable_viscosity = dico.variable_viscosity[0]
        self.v_visco_ref_visco1 = None
        self.v_visco_ref_temp1 = None
        self.v_visco_suther_temp1 = None

        self.v_visco_ref_visco2 = None
        self.v_visco_ref_temp2 = None
        self.v_visco_suther_temp2 = None

    def read_file(self, path):
        """
        Load the input file data in the class
        :param path: path of the run folder of diva
        :return: None
        """
        f = open(path + "/Input_File_Physical_Properties", "r")
        files = f.readlines()
        f.close()
        files = iter(files)
        for lines in files:
            if "*LIQUID PHASE" in lines:
                next(files)
                self.rho_liq = self.get_value(next(files), 1, v_type=float)
                self.mu_liq = self.get_value(next(files), 1, v_type=float)
            if "*GAS PHASE" in lines:
                next(files)
                self.rho_vap = self.get_value(next(files), 1, v_type=float)
                self.mu_vap = self.get_value(next(files), 1, v_type=float)
            if "*INTERFACE PHYSICAL PROPERTIES" in lines:
                next(files)
                self.sigma = self.get_value(next(files), 1, v_type=float)
                self.contact_angle = self.get_value(next(files), 1, v_type=float)
            if "*CONSTANT ACCELERATION" in lines:
                next(files)
                g1 = self.get_value(next(files), 1, v_type=float)
                g2 = self.get_value(next(files), 1, v_type=float)
                g3 = self.get_value(next(files), 1, v_type=float)
                self.g = (g1, g2, g3)
            if "*Marangoni Parameters" in lines:
                self.marangoni_type = dico.marangoni[self.get_value(next(files), 1, v_type=int)]
                self.marangoni_surf_tens_grad = self.get_value(next(files), 2, v_type=float)
                self.marangoni_ref_T = self.get_value(next(files), 2, v_type=float)
                self.marangoni_ref_sigma_at_tref = self.get_value(next(files), 2, v_type=float)
            if "*VARIABLE GAS VISCOSITY" in lines:
                for i in range(4):
                    next(files)
                self.variable_viscosity = dico.variable_viscosity[self.get_value(next(files), 1, v_type=int)]
            if "*Sutherland Parameters Gas Specie 1" in lines:
                self.v_visco_ref_visco1 = self.get_value(next(files), 1, v_type=float)
                self.v_visco_ref_temp1 = self.get_value(next(files), 1, v_type=float)
                self.v_visco_suther_temp1 = self.get_value(next(files), 1, v_type=float)
            if "*Sutherland Parameters Gas Specie 2" in lines:
                self.v_visco_ref_visco2 = self.get_value(next(files), 1, v_type=float)
                self.v_visco_ref_temp2 = self.get_value(next(files), 1, v_type=float)
                self.v_visco_suther_temp2 = self.get_value(next(files), 1, v_type=float)

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




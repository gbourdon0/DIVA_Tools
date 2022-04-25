import modules.diva_input.dictionnary_diva as dico


class Numerical_Solver:
    def __init__(self):
        # Runge Kutta solver
        self.runge_kutta_scheme = None
        self.CFL_conv = None
        self.CFL_surf_tens = None

        # interface solver
        self.interface = None
        self.navier_stokes = None
        self.pressure = None
        self.viscous = None
        self.viscous_temporal_type = None
        self.viscous_dissip = None
        self.temperature = None
        self.phase_change = None
        self.mass_frac = None
        self.mass_frac_N = None
        self.GFM_velocity_div_corr = None
        self.GFM_temperature_extension = None
        self.iter_nb_extension = None
        self.writing_all_data_file = None

    def read_file(self, path):
        """
        Load the input file data in the class
        :param path: path of the run folder of diva
        :return: None
        """
        f = open(path + "/Input_File_Numerical_Solver", "r")
        files = f.readlines()
        f.close()
        files = iter(files)
        for lines in files:

            if "*RUNGE KUTTA SCHEME" in lines:
                for i in range(5): next(files)
                self.runge_kutta_scheme = dico.rk[self.get_value(next(files), 1, v_type=int)]
                self.CFL_conv = self.get_value(next(files), 1, v_type=float)
                self.CFL_surf_tens = self.get_value(next(files), 1, v_type=float)
            if "*INTERFACE SOLVER" in lines:
                for i in range(4): next(files)
                self.interface = dico.interface_solv[self.get_value(next(files), 1, v_type=int)]
            if "*NAVIER-STOKES SOLVER" in lines:
                for i in range(6): next(files)
                self.navier_stokes = dico.navier_stokes[self.get_value(next(files), 1, v_type=int)]
                for i in range(5): next(files)
                self.pressure = dico.pressure[self.get_value(next(files), 1, v_type=int)]

            if "*DISCRETIZATION OF THE VISCOUS TERMS" in lines:
                for i in range(5): next(files)
                self.viscous = dico.viscous[self.get_value(next(files), 1, v_type=int)]
            if "*IMPLICIT TEMPORAL DISCRETIZATION OF VISCOUS TERMS" in lines:
                for i in range(5): next(files)
                self.viscous_temporal_type = dico.time_discrt[self.get_value(next(files), 1, v_type=int)]
            if "*ENERGY VISCOUS DISSIPATION" in lines:
                for i in range(4): next(files)
                self.viscous_dissip = dico.viscous_dissip[self.get_value(next(files), 1, v_type=int)]
            if "*TEMPERATURE SOLVER" in lines:
                for i in range(4): next(files)
                self.temperature = dico.temperature[self.get_value(next(files), 1, v_type=int)]
            if "*PHASE CHANGE" in lines:
                for i in range(6): next(files)
                self.phase_change = dico.phase_change[self.get_value(next(files), 1, v_type=int)]
            if "*MASS FRACTION SOLVER" in lines:
                for i in range(4): next(files)
                self.mass_frac = dico.mass_frac[self.get_value(next(files), 1, v_type=int)]
                for i in range(3): next(files)
                self.mass_frac_N = dico.mass_frac[self.get_value(next(files), 1, v_type=float)]
            if "*GHOST VELOCITY EXTENSION" in lines:
                for i in range(4): next(files)
                self.GFM_velocity_div_corr = dico.GFM_div_corr[self.get_value(next(files), 1, v_type=int)]
            if "*GHOST TEMPERATURE EXTENSION" in lines:
                for i in range(6): next(files)
                self.GFM_temperature_extension = dico.GFM_temp_ext[self.get_value(next(files), 1, v_type=int)]
            if "*EXTENSION ITERATION NUMBER" in lines:
                next(files)
                self.iter_nb_extension = self.get_value(next(files), 1, v_type=int)
            if "*DEACTIVATE ALL WRITING OF DATA FILES" in lines:
                next(files)
                self.writing_all_data_file = dico.write_all_data[self.get_value(next(files), 1, v_type=int)]
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




import modules.diva_input.dictionnary_diva as dico
import numpy as np

class Initial_Condition:
    def __init__(self):
        self.fluid_obj_dim = None
        self.fluid_obj_center = None

        self.solid_obj_dim = None
        self.solid_obj_center = None

        self.backup = None
        self.benchmark = None

        self.v_init_enable = None
        self.v_init = None

        self.T_init_enable = None
        self.Ri_0 = None
        self.Tp_int = None
        self.Tp_inf = None

        self.mass_frac_init_enable = None
        self.Ym1_int = None
        self.Ym1_int = None

        self.T_immersed = None
        self.DT_sub = None

    def read_file(self, path):
        """
        :param path: path of the diva/run file
        :return: None, but load data in the class/
        """

        f = open(path + "/Input_File_Initial_Condition", "r")
        files = f.readlines()
        f.close()
        files = iter(files)
        for lines in files:

            if "*INITIAL RADIUS AND POSITION OF THE SPHERE" in lines:
                next(files)
                self.fluid_obj_dim = tuple(self.get_value(next(files), 3, v_type=float))
                self.fluid_obj_center = tuple(self.get_value(next(files), 3, v_type=float))
            if "*INITIAL RADIUS AND POSITION OF THE SOLID OBJECT" in lines:
                next(files)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.solid_obj_dim = (p1, p2, p3)
                self.solid_obj_center = tuple(self.get_value(next(files), 3, v_type=float))
            if "*BACK-UP FILE" in lines:
                self.backup = dico.backup[self.get_value(next(files), 1, v_type=int)]
            if "*Benchmark" in lines:
                self.benchmark = dico.benchmark[self.get_value(next(files), 1, v_type=int)]

            if "*INITIAL CONDITION VELOCITY" in lines:
                next(files)
                self.v_init_enable = dico.v_init[self.get_value(next(files), 1, v_type=int)]
                self.v_init = self.get_value(next(files), 1, v_type=float)
            if "*Temperature Tp" in lines:
                self.T_init_enable = dico.T_init[self.get_value(next(files), 1, v_type=int)]
                self.Ri_0 = self.get_value(next(files), 1, v_type=float)
                self.Tp_int = self.get_value(next(files), 1, v_type=float)
                self.Tp_inf = self.get_value(next(files), 1, v_type=float)

            if "*Mass Fraction Ym1" in lines:
                self.mass_frac_init_enable = dico.mass_frac_init[self.get_value(next(files), 1, v_type=int)]
                self.Ym1_int = self.get_value(next(files), 1, v_type=float)
                self.Ym1_int = self.get_value(next(files), 1, v_type=float)

            if "*Temperature Immersed Boundary" in lines:
                self.T_immersed = self.get_value(next(files), 1, v_type=float)
            if "*Subcooled temperature liquid" in lines:
                self.DT_sub = self.get_value(next(files), 1, v_type=float)

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
            if "!" in value:
                value = np.nan
            else:
                if v_type == float:
                    value = float(value)
                if v_type == int:
                    value = int(value)
            return value

        for i in range(nb_value):
            value = line[i]
            if "d" in value:
                value = value.replace("d", "e")
            if "!" in value:
                value = np.nan
            else:
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




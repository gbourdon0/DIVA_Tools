import modules.diva_input.dictionnary_diva as dico


class Mass_Fraction_Boundary_Condition:
    def __init__(self):
        # Type of conditions
        self.BCX1 = None
        self.BCXN = None
        self.BCY1 = None
        self.BCYN = None
        self.BCZ1 = None
        self.BCZN = None

        # dirichlet conditions value
        self.BCX1_dir = None
        self.BCXN_dir = None
        self.BCY1_dir = None
        self.BCYN_dir = None
        self.BCZ1_dir = None
        self.BCZN_dir = None

        # neumann condition value
        self.BCX1_neu = None
        self.BCXN_neu = None
        self.BCY1_neu = None
        self.BCYN_neu = None
        self.BCZ1_neu = None
        self.BCZN_neu = None

    def read_file(self, path):
        f = open(path + "/Input_File_Mass_Fraction_Boundary_Condition", "r")
        files = f.readlines()
        f.close()
        files = iter(files)
        for lines in files:

            if "*TYPE OF BOUNDARY CONDITIONS" in lines:
                for i in range(8): next(files)
                self.BCX1 = dico.BC_mass_frad[self.get_value(next(files), 1, v_type=int)]
                self.BCXN = dico.BC_mass_frad[self.get_value(next(files), 1, v_type=int)]
                self.BCY1 = dico.BC_mass_frad[self.get_value(next(files), 1, v_type=int)]
                self.BCYN = dico.BC_mass_frad[self.get_value(next(files), 1, v_type=int)]
                self.BCZ1 = dico.BC_mass_frad[self.get_value(next(files), 1, v_type=int)]
                self.BCZN = dico.BC_mass_frad[self.get_value(next(files), 1, v_type=int)]

            if "*UNIFORM DIRICHLET BOUNDARY CONDITIONS" in lines:
                next(files)
                self.BCX1_dir = self.get_value(next(files), 1, v_type=float)
                self.BCXN_dir = self.get_value(next(files), 1, v_type=float)
                self.BCY1_dir = self.get_value(next(files), 1, v_type=float)
                self.BCYN_dir = self.get_value(next(files), 1, v_type=float)
                self.BCZ1_dir = self.get_value(next(files), 1, v_type=float)
                self.BCZN_dir = self.get_value(next(files), 1, v_type=float)

            if "*UNIFORM NEUMANN BOUNDARY CONDITIONS" in lines:
                next(files)
                self.BCX1_neu = self.get_value(next(files), 1, v_type=float)
                self.BCXN_neu = self.get_value(next(files), 1, v_type=float)
                self.BCY1_neu = self.get_value(next(files), 1, v_type=float)
                self.BCYN_neu = self.get_value(next(files), 1, v_type=float)
                self.BCZ1_neu = self.get_value(next(files), 1, v_type=float)
                self.BCZN_neu = self.get_value(next(files), 1, v_type=float)
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

    def get_X1_BC(self, rtype=tuple):
        """
        Return BC on X1
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on X1
        """
        if rtype == tuple:
            return self.BCX1, self.BCX1_dir, self.BCX1_neu
        if rtype == str:
            out = "Mass fraction : "
            if self.BCX1 == dico.BC_temperature[1]:
                out += dico.BC_temperature[1] + ", " + str(self.BCX1_dir)
            elif self.BCX1 == dico.BC_temperature[3]:
                out += dico.BC_temperature[3] + ", " + str(self.BCX1_neu)
            else:
                raise NotImplemented(
                    "For this choice, function are not implement yet. Only uniform Neumann and Dirichlet are")
            return out

        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_XN_BC(self, rtype=tuple):
        """
        Return BC on XN
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on XN
        """

        if rtype == tuple:
            return self.BCXN, self.BCXN_dir, self.BCXN_neu
        if rtype == str:
            out = "Mass fraction : "
            if self.BCXN == dico.BC_temperature[1]:
                out += dico.BC_temperature[1] + ", " + str(self.BCXN_dir)
            elif self.BCXN == dico.BC_temperature[3]:
                out += dico.BC_temperature[3] + ", " + str(self.BCXN_neu)
            else:
                raise NotImplemented(
                    "For this choice, function are not implement yet. Only uniform Neumann and Dirichlet are")
            return out

        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_Y1_BC(self, rtype=tuple):
        """
        Return BC on Y1
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on Y1
        """
        if rtype == tuple:
            return self.BCY1, self.BCY1_dir, self.BCY1_neu
        if rtype == str:
            out = "Mass fraction : "
            if self.BCY1 == dico.BC_temperature[1]:
                out += dico.BC_temperature[1] + ", " + str(self.BCY1_dir)
            elif self.BCY1 == dico.BC_temperature[3]:
                out += dico.BC_temperature[3] + ", " + str(self.BCY1_neu)
            else:
                raise NotImplemented(
                    "For this choice, function are not implement yet. Only uniform Neumann and Dirichlet are")
            return out

        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_YN_BC(self, rtype=tuple):
        """
        Return BC on YN
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on YN
        """
        if rtype == tuple:
            return self.BCYN, self.BCYN_dir, self.BCYN_neu
        if rtype == str:
            out = "Mass fraction : "
            if self.BCYN == dico.BC_temperature[1]:
                out += dico.BC_temperature[1] + ", " + str(self.BCYN_dir)
            elif self.BCYN == dico.BC_temperature[3]:
                out += dico.BC_temperature[3] + ", " + str(self.BCYN_neu)
            else:
                raise NotImplemented(
                    "For this choice, function are not implement yet. Only uniform Neumann and Dirichlet are")
            return out

        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_Z1_BC(self, rtype=tuple):
        """
        Return BC on ZN
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on ZN
        """
        if rtype == tuple:
            return self.BCZ1, self.BCZ1_dir, self.BCZ1_neu
        if rtype == str:
            out = "Mass fraction : "
            if self.BCZ1 == dico.BC_temperature[1]:
                out += dico.BC_temperature[1] + ", " + str(self.BCZ1_dir)
            elif self.BCZ1 == dico.BC_temperature[3]:
                out += dico.BC_temperature[3] + ", " + str(self.BCZ1_neu)
            else:
                raise NotImplemented(
                    "For this choice, function are not implement yet. Only uniform Neumann and Dirichlet are")
            return out

        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_ZN_BC(self, rtype=tuple):
        """
        Return BC on Z1
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on Z1
        """
        if rtype == tuple:
            return self.BCZN, self.BCZN_dir, self.BCZN_neu
        if rtype == str:
            out = "Mass fraction : "
            if self.BCZN == dico.BC_temperature[1]:
                out += dico.BC_temperature[1] + ", " + str(self.BCZN_dir)
            elif self.BCZN == dico.BC_temperature[3]:
                out += dico.BC_temperature[3] + ", " + str(self.BCZN_neu)
            else:
                raise NotImplemented(
                    "For this choice, function are not implement yet. Only uniform Neumann and Dirichlet are")
            return out

        else:
            raise Exception("Unknown type specified. Should be tuple or str")




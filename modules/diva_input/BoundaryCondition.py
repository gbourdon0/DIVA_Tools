import modules.diva_input.dictionnary_diva as dico


class BoundaryCondition:
    """
    A class that import and store the boundary condition for velocity store in the :
    Input_File_Boundary_Condition file from diva/run
    """

    def __init__(self):

        # BC : Boundary Condition
        # X1 = Y (or ZY) plan for the lowest Y value
        # See how it is done in DIVA, it's the same
        self.BCX1 = None
        self.BCXN = None
        self.BCY1 = None
        self.BCYN = None
        self.BCZ1 = None
        self.BCZN = None

        # turb stands for turbulent
        self.BC_turb_X1 = None
        self.BC_turb_XN = None
        self.BC_turb_Y1 = None
        self.BC_turb_YN = None
        self.BC_turb_Z1 = None
        self.BC_turb_ZN = None

        # int_length stand for integral length
        self.BC_int_length_X1 = None
        self.BC_int_length_XN = None
        self.BC_int_length_Y1 = None
        self.BC_int_length_Yn = None
        self.BC_int_length_Z1 = None
        self.BC_int_length_ZN = None

        # Value of velocity injection
        self.BC_X1 = (0, 0, 0)
        self.BC_XN = (0, 0, 0)
        self.BC_Y1 = (0, 0, 0)
        self.BC_YN = (0, 0, 0)
        self.BC_Z1 = (0, 0, 0)
        self.BC_Zn = (0, 0, 0)

    def read_file(self, path):
        """
        :param path: path of the diva/run file
        :return: None, but load data in the class/
        """

        f = open(path + "/Input_File_Boundary_Condition", "r")
        files = f.readlines()
        f.close()
        files = iter(files)

        # Use the structure of input file to find the values
        for lines in files:
            if "*BOUNDARY CONDITIONS FOR NAVIER STOKES AND INTERFACE" in lines:
                for i in range(7): next(files)
                self.BCX1 = dico.BC_vitesse[self.get_value(next(files), 1, v_type=int)]
                self.BCXN = dico.BC_vitesse[self.get_value(next(files), 1, v_type=int)]
                self.BCY1 = dico.BC_vitesse[self.get_value(next(files), 1, v_type=int)]
                self.BCYN = dico.BC_vitesse[self.get_value(next(files), 1, v_type=int)]
                self.BCZ1 = dico.BC_vitesse[self.get_value(next(files), 1, v_type=int)]
                self.BCZN = dico.BC_vitesse[self.get_value(next(files), 1, v_type=int)]
                for i in range(4): next(files)
                self.BC_turb_X1 = dico.BC_vitesse_turb[self.get_value(next(files), 1, v_type=int)]
                self.BC_turb_XN = dico.BC_vitesse_turb[self.get_value(next(files), 1, v_type=int)]
                self.BC_turb_Y1 = dico.BC_vitesse_turb[self.get_value(next(files), 1, v_type=int)]
                self.BC_turb_YN = dico.BC_vitesse_turb[self.get_value(next(files), 1, v_type=int)]
                self.BC_turb_Z1 = dico.BC_vitesse_turb[self.get_value(next(files), 1, v_type=int)]
                self.BC_turb_ZN = dico.BC_vitesse_turb[self.get_value(next(files), 1, v_type=int)]
            if "*INTEGRAL LENGHT" in lines:
                next(files)
                self.BC_int_length_X1 = self.get_value(next(files), 3, v_type=float)
                self.BC_int_length_XN = self.get_value(next(files), 3, v_type=float)
                self.BC_int_length_Y1 = self.get_value(next(files), 3, v_type=float)
                self.BC_int_length_YN = self.get_value(next(files), 3, v_type=float)
                self.BC_int_length_Z1 = self.get_value(next(files), 3, v_type=float)
                self.BC_int_length_ZN = self.get_value(next(files), 3, v_type=float)
            if "*INJECTION BOUNDARY CONDITIONS" in lines:
                next(files)
                next(files)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.BC_X1 = (p1, p2, p3)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.BC_XN = (p1, p2, p3)
                next(files)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.BC_Y1 = (p1, p2, p3)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.BC_YN = (p1, p2, p3)
                next(files)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.BC_Z1 = (p1, p2, p3)
                p1 = self.get_value(next(files), 1, v_type=float)
                p2 = self.get_value(next(files), 1, v_type=float)
                p3 = self.get_value(next(files), 1, v_type=float)
                self.BC_Zn = (p1, p2, p3)
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

    # get boundary conditions
    def get_X1_BC(self, rtype=tuple):
        """
        Return BC on X1
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on X1
        """
        if rtype == tuple:
            return self.BCX1, self.BC_X1, self.BC_turb_X1, self.BC_int_length_X1
        if rtype == str:
            out = "Velocity : "
            if self.BCX1 == dico.BC_vitesse[5]:
                out += dico.BC_vitesse[5] + ", " + str(self.BC_X1) + " m/s"
                if self.BC_turb_X1 == dico.BC_vitesse_turb[1]:
                    out += ", "+dico.BC_vitesse_turb[1] + ", " + str(self.BC_int_length_X1) + " m"
                else:
                    out += ", " +self.BC_turb_X1
            else:
                out += self.BCX1



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
            return self.BCXN, self.BC_XN, self.BC_turb_XN, self.BC_int_length_XN

        if rtype == str:
            out = "Velocity : "
            if self.BCXN == dico.BC_vitesse[5]:
                out += dico.BC_vitesse[5] + ", " + str(self.BC_XN) + " m/s"
                if self.BC_turb_XN == dico.BC_vitesse_turb[1]:
                    out += ","+dico.BC_vitesse_turb[1] + ", " + str(self.BC_int_length_XN) + " m"
                else:
                    out +=", " + self.BC_turb_XN
            else:
                out += self.BCXN


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
            return self.BCY1, self.BC_Y1, self.BC_turb_Y1, self.BC_int_length_Y1
        if rtype == str:
            out = "Velocity : "
            if self.BCY1 == dico.BC_vitesse[5]:
                out += dico.BC_vitesse[5] + ", " + str(self.BC_Y1) + " m/s"
                if self.BC_turb_Y1 == dico.BC_vitesse_turb[1]:
                    out += ", "+ dico.BC_vitesse_turb[1] + ", " + str(self.BC_int_length_Y1) + " m"
                else:
                    out += ", " + self.BC_turb_Y1
            else:
                out += self.BCY1

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
            return self.BCYN, self.BC_YN, self.BC_turb_YN, self.BC_int_length_YN

        if rtype == str:
            out = "Velocity : "
            if self.BCYN == dico.BC_vitesse[5]:
                out += dico.BC_vitesse[5] + ", " + str(self.BC_YN) + " m/s"
                if self.BC_turb_YN == dico.BC_vitesse_turb[1]:
                    out += ", "+dico.BC_vitesse_turb[1] + ", " + str(self.BC_int_length_YN) + " m"
                else:
                    out += ", " +self.BC_turb_YN
            else:
                out += self.BCYN

            return out
        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_Z1_BC(self, rtype=tuple):
        """
        Return BC on Z1
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on Z1
        """
        if rtype == tuple:
            return self.BCZ1, self.BC_Z1, self.BC_turb_Z1, self.BC_int_length_Z1
        if rtype == str:
            out = "Velocity : "
            if self.BCZ1 == dico.BC_vitesse[5]:
                out += dico.BC_vitesse[5] + ", " + str(self.BC_Z1) + " m/s"
                if self.BC_turb_Z1 == dico.BC_vitesse_turb[1]:
                    out += ", "+dico.BC_vitesse_turb[1] + ", " + str(self.BC_int_length_Z1) + " m"
                else:
                    out += ", " +self.BC_turb_Z1
            else:
                out += self.BCZ1

            return out
        else:
            raise Exception("Unknown type specified. Should be tuple or str")

    def get_ZN_BC(self, rtype=tuple):
        """
        Return BC on ZN
        :param rtype: return type, could be a tuple or a string (for human language)
        :return: return the BC on ZN
        """
        if rtype == tuple:
            return self.BCZN, self.BC_ZN, self.BC_turb_ZN, self.BC_int_length_ZN

        if rtype == str:
            out = "Velocity : "
            if self.BCZN == dico.BC_vitesse[5]:
                out += dico.BC_vitesse[5] + ", " + str(self.BC_ZN) + " m/s"
                if self.BC_turb_ZN == dico.BC_vitesse_turb[1]:
                    out += ", "+ dico.BC_vitesse_turb[1] + ", " + str(self.BC_int_length_ZN) + " m"
                else:
                    out +=", " + self.BC_turb_ZN
            else:
                out += self.BCZN
            return out
        else:
            raise Exception("Unknown type specified. Should be tuple or str")

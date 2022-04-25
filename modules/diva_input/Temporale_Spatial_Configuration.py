import modules.diva_input.dictionnary_diva as dico


class Temporal_Spatial_Configuration:
    def __init__(self):
        self.coord_system = dico.coord_sys[1]
        self.mesh = (0, 0, 0)
        self.gsize = (0, 0, 0)  # m
        self.end_time = 0
        self.nb_plot = 0
        self.max_iter = 0
        self.proc = (0, 0, 0)
        self.nb_proc = sum(self.proc)
        self.moving_ref = (0, 0, 0)
        self.mesh_type = (dico.mesh_type[0], dico.mesh_type[0], dico.mesh_type[0])
        self.mesh_non_u = (None, None, None)
        self.mirror_grid = (0, 0, 0)
        self.nb_zone_u_mesh = (0, 0, 0)
        self.inclusion_s = False
        self.inclusion_f = False
        self.drop_or_bubbles = dico.drop_or_bubbles[0]
        self.level_set_mass_cor = False
        self.immersed_boundary = dico.immersed_boundary[0]

    def read_file(self, path):
        """
        Load the input file data in the class
        :param path: path of the run folder of diva
        :return: None
        """
        f = open(path + "/Input_File_Temporal_Spatial_Configuration", "r")
        files = f.readlines()
        f.close()
        files = iter(files)
        for lines in files:
            if "*COORDINATE SYSTEM" in lines:
                value = self.get_value(next(files), 1, v_type=int)
                self.coord_system = dico.coord_sys[value]
            if "*NUMBER OF GRID POINTS" in lines:
                value = self.get_value(next(files), 3, v_type=int)
                self.mesh = (value[0], value[1], value[2])
            if "*SIZE OF THE COMPUTATIONAL FIELD" in lines:
                value = self.get_value(next(files), 3, v_type=float)
                self.gsize = (value[0], value[1], value[2])
            if "*FINAL TIME OF THE SIMULATION" in lines:
                value = self.get_value(next(files), 1, v_type=float)
                self.end_time = value
            if "*NUMBER OF COMPUTATIONAL ZONES IN THE ANIMATE FILES" in lines:
                value = self.get_value(next(files), 1, v_type=int)
                self.nb_plot = value
            if "*MAXIMUM NUMBER OF TEMPORAL ITERATIONS" in lines:
                value = self.get_value(next(files), 1, v_type=int)
                self.max_iter = value
            if "*NUMBER OF CORES FOR A PARALLEL RUN" in lines:
                value = self.get_value(next(files), 1, v_type=int)
                value1 = self.get_value(next(files), 1, v_type=int)
                value2 = self.get_value(next(files), 1, v_type=int)
                self.proc = (value, value1, value2)
                self.nb_proc = sum(self.proc)
            if "*RELATIVE REFERENCE SYSTEM" in lines:
                next(files)
                value = self.get_value(next(files), 1, v_type=float)
                value1 = self.get_value(next(files), 1, v_type=float)
                value2 = self.get_value(next(files), 1, v_type=float)
                self.moving_ref = (value, value1, value2)
            if "*KIND OF MESH" in lines:
                for i in range(5):  # skip 5 lines
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                value1 = self.get_value(next(files), 1, v_type=int)
                value2 = self.get_value(next(files), 1, v_type=int)
                self.mesh_type = self.apply_dico(dico.mesh_type, (value, value1, value2))
            if "*FUNCTION FOR THE NON UNIFORM GRID" in lines:
                for i in range(6):  # skip 6 lines
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                value1 = self.get_value(next(files), 1, v_type=int)
                value2 = self.get_value(next(files), 1, v_type=int)
                self.mesh_non_u = self.apply_dico(dico.mesh_non_u, (value, value1, value2))
            if "*MIRROR GRID" in lines:
                for i in range(4):
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                value1 = self.get_value(next(files), 1, v_type=int)
                value2 = self.get_value(next(files), 1, v_type=int)
                self.mirror_grid = self.apply_dico(dico.mesh_mirror, (value, value1, value2))
            if "*ZONE NUMBER FOR A MIXED GRID" in lines:
                for i in range(3):
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                value1 = self.get_value(next(files), 1, v_type=int)
                value2 = self.get_value(next(files), 1, v_type=int)
                self.nb_zone_u_mesh = (value, value1, value2)
            if "*NUMBER OF INCLUSION" in lines:
                for i in range(4):
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                self.inclusion_f = value
                value = self.get_value(next(files), 1, v_type=int)
                self.inclusion_s = value
            if "*DROPS OR BUBBLES" in lines:
                for i in range(5):
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                self.drop_or_bubbles = dico.drop_or_bubbles[value]
            if "*IMMERSED BOUNDARY" in lines:
                for i in range(5):
                    next(files)
                value = self.get_value(next(files), 1, v_type=int)
                self.immersed_boundary = dico.immersed_boundary[value]
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

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt


class PicklePLT:
    """
    A simple class to read matplotlib plot saved in a .pickle file.
    """

    def __init__(self):
        """
        fig : a matplolib fig object
        axes : axes matplotlib object
        data : a list of dictionnary. data[0] = dictionnary containing data for the 1st axes.
        lines : a list of dictionnary. data[0] = ictionnary containg matplotlib line object for the 1st axis
        """
        self.nb_axe = 0
        self.axes = []
        self.title = ""
        self.fig = None
        self.data = []
        self.lines = []
        self.polyline = []
        self.annotation = []
        #Matplotlib types
        self.PolyCollection = "<class 'matplotlib.collections.PolyCollection'>"
        self.Line = "<class 'matplotlib.lines.Line2D'>"
        self.Annotation = "<class 'matplotlib.text.Annotation'>"
    def load_pickle(self, path):
        """
        load a pickle file containg matplotlib data
        :param path: path of the file
        :return: fig,ax
        """
        self.fig = pickle.load(open(path, 'rb'))
        self.axes = self.fig.get_axes()
        print(f"{len(self.axes)} subplot(s) founded.")

        # Treating axes

        for axe in self.axes:
            lines = axe.lines
            children = axe._children
            ddata = {} #general data
            dline = {} #lines data
            dpoly = {} #polycollections data
            danot = {} #annotation data
            l_num = 0
            for child in children:
                if str(type(child)) == self.Line:
                    line = lines[l_num]
                    l_num += 1
                    label = line.get_label()  # If no label, should be something libe _child1 by default
                    dline[label] = line
                    data = line.get_data()
                    ddata[label] = data
                elif str(type(child)) == self.PolyCollection:
                    label = child._label
                    to_sort = child._paths[0]._vertices[1:-1]
                    middle = len(to_sort) // 2 + 1
                    y1 = to_sort[:middle - 1][:, 1]
                    y2 = to_sort[middle:]
                    y2 = np.flip(y2, axis=0)
                    x1 = np.array(list(y2[:, 0]))
                    y2 = y2[:, 1]
                    ddata[label] = np.array([x1, y1, y2])
                    dpoly[label] = child
                elif str(type(child)) == self.Annotation:
                    danot[child._label] = child
                    ddata[child._label] = None
            # store in the class data and the class obj
            self.data.append(ddata)
            self.lines.append(dline)
            self.polyline.append(dpoly)
            self.annotation.append(danot)
        return self.fig, self.axes

    def get_data(self, axes, look):
        """
        Access data of the axes
        :param axes: number of the wished axis
        :param look: if int, the number of the line, if str, the label of the line (same as in the legend)
        :return: 2d array with x and y data
        """
        if type(look) == str:
            return self.data[axes][look]
        elif type(look) == int:
            key = list(self.data[axes].keys())[look]
            return self.data[axes][key]
        else:
            raise Exception(f"'look' type not recognize. Should be string or int not {type(look)}")

    def get_lines(self, axes, look):
        """
        return the line object
        :param axes: number of the wished axis
        :param look: if int, the number of the line, if str, the label of the line (same as in the legend)
        :return:
                """
        if type(look) == str:
            return self.lines[axes][look]
        elif type(look) == int:
            print(self.lines[axes])
            key = list(self.lines[axes].keys())[look]
            return self.lines[axes][key]
        else:
            raise Exception(f"'look' type not recognize. Should be string or int not {type(look)}")

    def get_poly_collection(self, axes, look):
        """
        return the line object
        :param axes: number of the wished axis
        :param look: if int, the number of the line, if str, the label of the line (same as in the legend)
        :return:
                """
        if type(look) == str:
            return self.polyline[axes][look]
        elif type(look) == int:
            print(self.polyline[axes])
            key = list(self.polyline[axes].keys())[look]
            return self.polyline[axes][key]
        else:
            raise Exception(f"'look' type not recognize. Should be string or int not {type(look)}")

    def get_annotation(self, look,axes = 0):
        """
        return the line object
        :param axes: number of the wished axis
        :param look: if int, the number of the line, if str, the label of the line (same as in the legend)
        :return:
                """
        if type(look) == str:
            return self.annotation[axes][look]
        elif type(look) == int:
            print(self.annotation[axes])
            key = list(self.annotation[axes].keys())[look]
            return self.annotation[axes][key]
        else:
            raise Exception(f"'look' type not recognize. Should be string or int not {type(look)}")

    def get_data_header(self):
        out = []
        for elem in self.data:
            out.append(list(elem.keys()))
        print(out)
        return out
    def move_annotation(self,label, x = None, y = None, axes = 0):
        ano = self.get_annotation(label,axes = axes)
        if x is not None:
            ano._x = x
        if y is not None:
            ano._y = y

    def move_axes(self,ax, fig, twin = None, subplot_spec=111):

        """Move an Axes object from a figure to a new pyplot managed Figure in
        the specified subplot.
        from https://gist.github.com/salotz/8b4542d7fe9ea3e2eacc1a2eef2532c5"""

        # get a reference to the old figure context so we can release it
        old_fig = ax.figure

        # remove the Axes from it's original Figure context
        ax.remove()

        # set the pointer from the Axes to the new figure
        ax.figure = fig


        # add the Axes to the registry of axes for the figure
        fig.axes.append(ax)
        # twice, I don't know why...
        fig.add_axes(ax)
        # then to actually show the Axes in the new figure we have to make
        # a subplot with the positions etc for the Axes to go, so make a
        # subplot which will have a dummy Axes
        dummy_ax = fig.add_subplot(subplot_spec)

        # then copy the relevant data from the dummy to the ax
        ax.set_position(dummy_ax.get_position())


        # then remove the dummy
        dummy_ax.remove()
        if twin != None:
            ax_bis = ax.twiny()
            ax_bis.set_xlabel(r"$\Theta$ (deg)")
        # close the figure the original axis was bound to
        plt.close(old_fig)



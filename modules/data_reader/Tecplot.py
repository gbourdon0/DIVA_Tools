from typing import List, Any

import pandas as pd
import numpy as np
import os  # It is supposed that frames are added by growing time
from modules.data_reader.plt_obj import plt_obj as plt_reader
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection


class Tecplot:
    dx: list[float]
    dy: list[float]

    def __init__(self):
        self.nb_frames = 0
        self.frames = {}
        self.time_to_frame = {}
        self.time = []
        self.extent = [0, 0, 0, 0,0,0]
        self.x_label = ''
        self.y_label = ''
        self.z_label = ''
        self.geom_type = ''
        self.dx = []
        self.dy = []
        self.dz = []

    # ******************Add functions

    def open_folder(self, path: str) -> None:
        """
        Load all the .plt file in a folder
        :param path: path of the animation file folder
        :return: None
        """
        # supposed that everything is sort by growing time
        print(f"Opening plt in {path}")
        filelist = os.listdir(path)
        filelist.sort()
        for files in filelist:
            if not ".plt" in files:
                pass
            else:
                self.add_frame(path + "/" + files)
        print(f"{self.nb_frames} plots imported.")
        self.get_geom_type()

    def add_frame(self, path) -> None:
        """
        add a .plt to the Tecplot object
        :param path: path of a .plt file
        :return: None
        """
        if ".plt" in path:
            frame = plt_reader(path)
            self.nb_frames += 1
            # frame should be a plt_obj
            self.frames[self.nb_frames] = frame
            self.time_to_frame[frame.time] = self.nb_frames
            self.get_geom_type()
        return None

    def add_frame_list(self, path_list: list[str]) -> None:
        """
        Add .plt files according the path_list
        :param path_list: list of path of .plt file
        :return: None
        """
        for path in path_list:
            self.add_frame(path)

    def add_variable_to_frame(self, frame: int, var_name: str, var: list) -> None:
        """
        Add a variable to a frame
        :param frame: frame number
        :param var_name: name of the variable
        :param var: list with the variables values. Should be the same length as other columns of the dataset
        :return:None
        """
        self[frame][var_name] = var

    def add_grid_to_frame(self, frame: int, var_name: str, grid):
        """
        Add a grid (matrix of dimension mesh_dim) to the data
        :param frame: frame number
        :param var_name: variable name
        :return:
        """
        if self.geom_type == "2D" or self.geom_type == "2D_axi":
            self[frame][var_name] = grid.reshape(self[frame].mesh_dim[0] * self[frame].mesh_dim[1])

    # ******************get functions

    def get_geom_type(self, forced=False) -> None:
        """
        Catch the geometry type of the .plt for a .plt from DIVA. This is done according the header of the .plt file
        :return: None
        """
        if self.nb_frames == 1 or forced == True:  # Only need to do it at the first.plt

            if "R" in self.get_header() and "Z" in self.get_header():
                self.geom_type = "2D_axi"
                # initialize extent for plotting
                f = self[1]
                self.x_label = "R"
                self.y_label = "Z"
                # compute dx
                x = np.array((self[1]["R"]))
                y = np.array((self[1]["Z"]))
                y = y.reshape(self[1].mesh_dim[1], self[1].mesh_dim[0])
                x = x.reshape(self[1].mesh_dim[1], self[1].mesh_dim[0])
                # compute as a list if the mesh is non uniform
                self.dy = np.gradient(y, axis=0).reshape(self[1].mesh_dim[1] * self[1].mesh_dim[0])
                self.dx = np.gradient(x, axis=1).reshape(self[1].mesh_dim[1] * self[1].mesh_dim[0])

                # extent is used to plot 2D values

                self.extent = [min(f["R"]) - self.dx[0] / 2, max(f["R"]) - self.dx[-1] / 2,
                               min(f["Z"]), max(f["Z"])]
            elif "X" in self.get_header() and "Y" in self.get_header() and "Z" not in self.get_header():
                self.geom_type = "2D"
                # initialize extent for plotting
                f = self[1]
                self.x_label = "X"
                self.y_label = "Y"
                # compute dx
                x = np.array((self[1]["X"]))
                y = np.array((self[1]["Y"]))
                y = y.reshape(self[1].mesh_dim[1], self[1].mesh_dim[0])
                x = x.reshape(self[1].mesh_dim[1], self[1].mesh_dim[0])
                # compute as a list if the mesh is non uniform
                self.dy = np.gradient(y, axis=0).reshape(self[1].mesh_dim[1] * self[1].mesh_dim[0])
                self.dx = np.gradient(x, axis=1).reshape(self[1].mesh_dim[1] * self[1].mesh_dim[0])
                # extent is used to plot 2D values

                self.extent = [min(f["X"]) - self.dx[0] / 2, max(f["X"]) - self.dx[-1] / 2,
                               min(f["Y"]), max(f["Y"])]
            else:  # Because I'm lazy and I've done only for my case (selfish ...)
                raise NotImplementedError(f"This type of geometry is not implemented : {self.geom_type}.")

    def get_frame_time(self, look_time: float):
        """
        return the nearest frame for a given time
        :param look_time: time we are looking for
        :return: plt_obj with the nearest type from look_time
        """
        # Return the frame with the nearest time
        keys = np.array(list(self.time_to_frame.keys()))  # get time list
        dif = np.absolute(keys - look_time)
        return self.frames[dif.argmin() + 1]  # since we began to enumerate frame from 1, and numpy from 0

    def get_header(self) -> [str]:
        """
        :return: list of variables in the .plt files
        """
        try:
            return list(self[1].data.columns)
        except:
            raise Exception("Tecplot has no frame loaded. Please try to load at least one frame")

    def get_interpolated(self, frame, var_name, x=[], y=[], itype='cubic'):
        """
        :param frame: frame number
        :param var_name: variable name
        :param x: list of x where the data is interpolated
        :param y:  list of y where the data is interpolated
        :param itype: interpolation type (cubic, linear)
        :return: list of interpolated values
        """
        xx, yy = self[frame][self.x_label], self[frame][self.y_label]
        from scipy import interpolate
        points = np.transpose(np.vstack((xx, yy)))
        out = interpolate.griddata(points, self[frame][var_name], (x, y),
                                   method=itype, rescale=True)
        return out

    def get_iso_value_2D(self, frame, var_name, iso_values=None):
        """
        For a given field, return list with all the location of the iso_values[].
        If there is more than 1 iso values line, return the location for the longer line
        Example : if there is bubble and a vapor film, the isovalues for phi = 0 is not a continuous line but
        there is a line for the bubble and for the film. The return value will be the one with the longest perimeter
        :param frame: frame number
        :param var_name: variable name
        :param iso_values: iso values list. Actually should be a list of one element
        :return: x,y, the x,y location of the iso value
        """
        if iso_values is None:
            iso_values = []
        if type(frame) == int:
            try:
                frame = self[frame]
            except:
                raise Exception("Specified frame number is out of range, deleted or not loaded")
        else:
            try:
                frame = self.get_frame_time(frame)
            except:
                raise Exception("Specified time is out of range, or no frame are loaded")
        if type(iso_values) != list:
            iso_value = [iso_values]
        var = frame[var_name]
        line_to_plot = var.reshape(frame.mesh_dim[1], frame.mesh_dim[0])
        cs = plt.contour(line_to_plot, [0], extent=self.extent)
        maxi = len(cs.collections[0].get_paths()[0])
        idx = 0
        for i in range(len(cs.collections[0].get_paths())):
            if len(cs.collections[0].get_paths()[i]) > maxi:
                maxi = len(cs.collections[0].get_paths()[i])
                idx = i
        p1 = cs.collections[0].get_paths()[idx]  # grab the 1st path
        v = p1.vertices
        x = v[:, 0]
        y = v[:, 1]
        plt.clf()
        plt.close()
        return x, y

    def get_film_interface(self, frame, phi_liq_name, phi_sol_name, method=1):
        """
        For a given field, return list with all the location of film boiling interface.
        If multiple bubbles, compute the geometric barycenter of each bubbles (including film), and return the one
        with the clothest barycenter as the solid interface
        :param method: choose method to find which path is the film (and not the bubbles).
        Method = 1 :  Compare the barycenter of the solid with the one of the path. The nearest is consider to be the film.
        Can some time do not work
        Method = 2 : Compare all the x and y compnent of the path with the barycenter of the solid. compute the minimum
         distance a path has with the solid barycenter. The path with the minimum of the minimum distance is assume to be the film
        :param phi_liq_name: phi_liq_name
        :param phi_sol_name: phi_solid name
        :param frame: frame number
        :param var_name: variable name
        :param iso_values: iso values list. Actually should be a list of one element
        :return: x,y, the x,y location of the iso value
        """
        frame_number = frame
        if type(frame) == int:
            try:
                frame = self[frame]
            except:
                raise Exception("Specified frame number is out of range, deleted or not loaded")
        else:
            try:
                frame = self.get_frame_time(frame)
            except:
                raise Exception("Specified time is out of range, or no frame are loaded")

        phi = frame[phi_liq_name]
        line_to_plot = phi.reshape(frame.mesh_dim[1], frame.mesh_dim[0])
        cs = plt.contour(line_to_plot, [0], extent=self.extent)

        x_phi_sol, y_phi_sol = self.get_iso_value_2D(frame_number, phi_sol_name, iso_values=None)
        if method == 1:
            bary_sol = np.array([np.mean(x_phi_sol), np.mean(y_phi_sol)])
            diff = []

            for elem in cs.collections[0].get_paths():
                v = elem.vertices
                x = v[:, 0]
                y = v[:, 1]
                bar = np.array([np.mean(x), np.mean(y)])
                diff.append(np.sum(np.sqrt((bary_sol - bar) ** 2)))

            idx = diff.index(min(diff))

            p1 = cs.collections[0].get_paths()[idx]  # grab the 1st path
            v = p1.vertices
            x = v[:, 0]
            y = v[:, 1]
            plt.clf()
            plt.close()
            return x, y
        elif method == 2:

            diff = []
            bary_sol = np.array([np.mean(x_phi_sol), np.mean(y_phi_sol)])
            for elem in cs.collections[0].get_paths():
                v = elem.vertices
                x = v[:, 0]
                y = v[:, 1]

                difx = np.absolute(x - bary_sol[0])
                dify = np.absolute(y - bary_sol[1])

                distance = np.absolute(x - bary_sol[0]) + np.absolute(y - bary_sol[1])
                distance = min(distance)
                diff.append(distance)

            idx = diff.index(min(diff))
            p1 = cs.collections[0].get_paths()[idx]  # grab the good path
            v = p1.vertices
            x = v[:, 0]
            y = v[:, 1]
            plt.clf()
            plt.close()
            return x, y

    def get_grid_data(self, frame=1, var_name=''):
        """
        return a matrix with dim mesh_dim and the wished field
        :param frame: frame number
        :param var_name: variable name
        :return:
        """
        if self.geom_type == "2D" or "2D_axi":
            # To get the grid, meshd_im are invert to fix in a matrix
            '''
                | a11  a12  a13  a14 ...  a1,nx-1 a1,nx   |
                | a11  a12  a13  a14 ...  a1,nx-1 a1,nx   |
                | .     .    .    .  ...     .      .     |
                | .     .    .    .  ...     .      .     |
                | .     .    .    .  ...     .      .     |
                | any1 any2 any3 any4...  any,nx-1 any,nx |
            
            --> size of matrix (ny,nx)
            '''
            if var_name == "dx":
                return self.dx.reshape(self[frame].mesh_dim[1], self[frame].mesh_dim[0])
            elif var_name == "dy":
                return self.dy.reshape(self[frame].mesh_dim[1], self[frame].mesh_dim[0])
            else:
                return self[frame][var_name].reshape(self[frame].mesh_dim[1], self[frame].mesh_dim[0])

    # ******************Remove functions

    def remove_frame(self, time=0, frame=0):
        """
        Remove of frame nearest the given time argument, or according its frame number
        :param time: time in second
        :param frame: frame number
        :return:
        """
        if time != 0:
            idx = self.time_to_frame[time]
            self.frames.pop(idx)
            self.time_to_frame.pop(time)
        elif frame != 0:
            time = self.frames[frame].time
            self.frames.pop(frame)
            self.time_to_frame.pop(time)
        else:
            raise Exception("No Input. No frame has been removed")
        return None

    def select_data_range(self, xrange, yrange, zrange=None):
        if self.geom_type in ["2D", "2D_axi"]:
            for i in range(1, self.nb_frames + 1):
                frame = self[i]
                frame.data = frame.data.loc[
                    (frame.data[self.x_label] > xrange[0]) & (frame.data[self.x_label] < xrange[1])]
                frame.data = frame.data.loc[
                    (frame.data[self.y_label] > yrange[0]) & (frame.data[self.y_label] < yrange[1])]
                nx = len(list(set(frame.data[self.x_label])))
                ny = len(list(set(frame.data[self.y_label])))
                frame.mesh_dim = (nx, ny, 1)
            self.get_geom_type(forced=True)
        return None

    # ****************** Reconstruction functions

    def from_axi_to_2D(self):
        """
        Reconstruct 2D field from a 2D axisymetric field
        :return:
        """
        print("Warning : for vector variable some change may be done in the Tecplot function. Change are taken into account"
              "for ughost_gas, ughost_liq and U_r. Please add correct names to have a good post treatment")
        for i in range(1, self.nb_frames + 1):
            frame = self[i]
            flipped = pd.DataFrame()
            header = frame.data.columns

            for head in header:
                signe = 1
                if head in ["R", "U_r", "ughost_gas", "ughost_liq"]:
                    signe = -1

                field = frame[head].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                r_field = signe * np.fliplr(field)
                # r_field = signe*np.lib.pad(field, ((0, 0), (0, 0)), 'reflect')
                conc = np.concatenate((r_field, field), axis=1)
                conc = conc.reshape(conc.shape[0] * conc.shape[1])
                flipped[head] = conc
            self[i].data = flipped
            self[i].mesh_dim = (self[i].mesh_dim[0] * 2, self[i].mesh_dim[1], self[i].mesh_dim[2])
            self[i].data.rename(columns={'Z': 'Y', 'R': 'X'}, inplace=True)
            self.x_label = "X"
            self.y_label = "Y"
        self.get_geom_type(forced=True)  # refresh dx, dy and extent
        self.geom_type = "2D"

    # def from_2D_to_3D(self, rot_number):
    #     """
    #     Reconstruct 3D field from a 2D fiel, rotation according y axes
    #     """
    #     def mat_rot_y_theta(theta):
    #         mat = np.array([
    #             [ np.cos(theta),0,np.sin(theta)],
    #             [0,1,0],
    #             [-np.sin(theta),0, np.cos(theta)]
    #         ])
    #     for i in range(1, self.nb_frames + 1):
    #         frame = self[i]
    #         for rot in rot_number:
    #             df = pd.DataFrame()
    #             header = frame.data.columns
    #             for head in header:



    # ****************** plot functions
    def plot(self, frame=1, flood='', cb_scale=[], vector=[], lines=[], lines_levels=[], vscale=0.1, scatter=[],
             mesh=False, iso_lines=[], disp_time=False, show=True, title='', zoom=None, vselect=None):
        """
                a quick integrated plot function to quick plot values
                :param cb_scale: color bar scale for flood plots
                :param frame: frame number
                :param flood: flood field (i.e with color map such as temperature)
                :param vector: [vx,vy], list of the name of the x component and y component of the vector. vx and vy are string
                which are in the header
                :param lines: plot lines from a field (by default plot for the isovalues 0). Should be a list of string
                :param lines_levels: list the wanted lines levels
                :param vscale: scale for the arrow of the vector (to have a good view)
                :param scatter: data to scatter
                :param mesh: if true, plot the mesh
                :param iso_lines:
                :return: fig and ax
                """
        if self.geom_type == "2D_axi":
            out = self.plot_2D_axi(frame, flood, cb_scale, vector, lines, lines_levels, vscale, scatter, mesh,
                                   iso_lines,
                                   disp_time, show, title=title, zoom=zoom, vselect=vselect)
        elif self.geom_type == "2D":
            out = self.plot_2D(frame, flood, cb_scale, vector, lines, lines_levels, vscale, scatter, mesh,
                               iso_lines,
                               disp_time, show, title, zoom, vselect = vselect)
        else:
            raise NotImplementedError("Plot is only implemented for 2D axi .plt file. Sorry I'm lazy.")

        return out

    def plot_2D_axi(self, frame=1, flood='', cb_scale=[], vector=[], lines=[], lines_levels=[], vscale=0.1, scatter=[],
                    mesh=False,
                    iso_lines=[], disp_time=False, show=True, title='', zoom=None, vselect=None):
        """
        a quick integrated plot function to quick plot values
        :param show: show or not the plot
        :param disp_time: disp simulation time on the plot
        :param cb_scale: color bar scale for flood plots
        :param frame: frame number
        :param flood: flood field (i.e with color map such as temperature)
        :param vector: [vx,vy], list of the name of the x component and y component of the vector. vx and vy are string
        which are in the header
        :param lines: plot lines from a field (by default plot for the isovalues 0). Should be a list of string
        :param lines_levels: list the wanted lines levels
        :param vscale: scale for the arrow of the vector (to have a good view)
        :param scatter: data to scatter
        :param mesh: if true, plot the mesh
        :param iso_lines: name of isolines to plot
        :param title: add a title to a plot
        :param zoom: should be [(xmin,xmax),(ymin,ymax)] to zoom on the figure
        :param vselect : For plotting take 1/vselect vector in x axis and 1/vselect vector in y-axis. Could make the plot
        more readable
        :return: fig and ax
        """
        from modules.global_variable.param import plot_param

        # Get the frame to plot
        import copy
        frame_num = copy.deepcopy(frame)
        if type(frame) == int:
            try:
                frame = self[frame]
            except:
                raise Exception("Specified frame number is out of range, deleted or not loaded")
        else:
            try:
                frame = self.get_frame_time(frame)
            except:
                raise Exception("Specified time is out of range, or no frame are loaded")

        fig, ax = plt.subplots(1, 1)
        # ax.legend(loc="lower center")
        # plot flood
        if flood in self.get_header():
            toplot = frame[flood].reshape(frame.mesh_dim[1], frame.mesh_dim[0])

            if cb_scale:
                img = ax.imshow(toplot, extent=self.extent, origin="lower", cmap=plot_param["cmap"], vmin=cb_scale[0]
                                , vmax=cb_scale[1])

                if len(cb_scale) < 3:
                    step = 10
                else:
                    step = cb_scale[2]
                delta = (cb_scale[1] - cb_scale[0]) / step
                ticks = [cb_scale[0] + delta * i for i in range(step + 1)]
                cb = fig.colorbar(img, ticks=ticks)
                cb.set_label(flood)
                ticks = ["{0:.2g}".format(cb_scale[0] + delta * i) for i in range(step + 1)]
                cb.ax.set_yticklabels(ticks)
            else:
                img = ax.imshow(toplot, extent=self.extent, origin="lower", cmap=plot_param["cmap"])
                cb = fig.colorbar(img)
                cb.set_label(flood)

        # scatter
        if scatter:
            try:
                x = frame[scatter[0]].reshape(frame.mesh_dim[0], frame.mesh_dim[1])
                y = frame[scatter[1]].reshape(frame.mesh_dim[0], frame.mesh_dim[1])
                scat = ax.scatter(x, y, s=1)
            except:
                scat = ax.scatter(scatter[0], scatter[1])

        # plot vector
        if vector:
            if vselect != None:

                vx = self.get_grid_data(var_name=vector[0], frame=frame_num)
                vy = self.get_grid_data(var_name=vector[1], frame=frame_num)
                x = self.get_grid_data(var_name=self.x_label, frame=frame_num)
                y = self.get_grid_data(var_name=self.y_label, frame=frame_num)

                sel1 = np.arange(0,vx.shape[0], vselect-1)
                vx = np.take(vx, sel1, axis=0)
                vy = np.take(vy, sel1, axis=0)
                x = np.take(x, sel1, axis=0)
                y = np.take(y, sel1, axis=0)

                sel1 = np.arange(0, vx.shape[1], vselect-1)
                vx = np.take(vx, sel1, axis=1)
                vy = np.take(vy, sel1, axis=1)
                x = np.take(x, sel1, axis=1)
                y = np.take(y, sel1, axis=1)

                ax.quiver(x, y, vx, vy, scale_units="xy", scale=vscale, width=plot_param["vector_linewidths"])
            else:
                vx = frame[vector[0]]
                vy = frame[vector[1]]
                ax.quiver(frame[self.x_label], frame[self.y_label], vx, vy, scale_units="xy", scale=vscale,
                          width=plot_param["vector_linewidths"])

        # mesh
        if mesh:
            set_x = list(set(frame[self.x_label] - self.dx / 2.0))
            set_y = list(set(frame[self.y_label] - self.dy / 2.0))
            x, y = np.meshgrid(set_x, set_y)

            # plt.scatter(x, y)

            segs1 = np.stack((x, y), axis=2)
            segs2 = segs1.transpose(1, 0, 2)
            plt.gca().add_collection(LineCollection(segs1, colors="k"))
            plt.gca().add_collection(LineCollection(segs2, colors="k"))

        # plot lines
        if lines:
            if not lines_levels:
                lines_levels = [0] * len(lines)  # Default value is 0
            k = 0
            labels = []
            color_set = ['k', 'tab:gray', 'tab:blue']
            for line in lines:
                line_to_plot = frame[line].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                ct = ax.contour(line_to_plot, levels=lines_levels[k], linewidths=plot_param["linewidths"],
                                linestyles=plot_param["linestyles"], zorder=plot_param["zorder"], extent=self.extent,
                                colors=color_set[k])
                labels.append(mpatches.Patch(color=color_set[k], label=line))

                if not type(lines_levels[k]) == int:  # disp line value on the graph if not default value
                    plt.clabel(ct, inline=1, fontsize=10)

                k += 1
            # plt.legend(handles=labels, loc = "lower center")

        # plot iso_lines
        if iso_lines:
            for line in iso_lines:
                line_to_plot = frame[line].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                ct = ax.contour(line_to_plot, linewidths=plot_param["linewidths"],
                                linestyles=plot_param["linestyles"], zorder=plot_param["zorder"], extent=self.extent)
            plt.clabel(ct, inline=1, fontsize=10)

        # display simulation time
        if disp_time:
            x_text = self.extent[0]
            y_text = self.extent[3] * 1.1
            text = "Time = " + str(frame.time) + " s"
            ax.text(x_text, y_text, text)
        if title != '':
            plt.title(title)
        # Put labels
        ax.set_xlabel(self.x_label + " [m]")
        ax.set_ylabel(self.y_label + " [m]")

        plt.axis('equal')
        plt.gca().set_aspect('equal', adjustable='box')

        if zoom != None:
            plt.xlim(zoom[0])
            plt.ylim(zoom[1])
        if show:
            plt.show()

        return fig, ax

    def plot_2D(self, frame=1, flood='', cb_scale=[], vector=[], lines=[], lines_levels=[], vscale=0.1, scatter=[],
                mesh=False,
                iso_lines=[], disp_time=False, show=True, title='', zoom=None, vselect=None):

        """
        a quick integrated plot function to quick plot values for 2D
        :param show: show or not the plot
        :param disp_time: disp simulation time on the plot
        :param cb_scale: color bar scale for flood plots
        :param frame: frame number
        :param flood: flood field (i.e with color map such as temperature)
        :param vector: [vx,vy], list of the name of the x component and y component of the vector. vx and vy are string
        which are in the header
        :param lines: plot lines from a field (by default plot for the isovalues 0). Should be a list of string
        :param lines_levels: list the wanted lines levels
        :param vscale: scale for the arrow of the vector (to have a good view)
        :param scatter: data to scatter
        :param mesh: if true, plot the mesh
        :param iso_lines: name of isolines to plot
        :param title: add a title to a plot
        :param zoom: should be [(xmin,xmax),(ymin,ymax)] to zoom on the figure
        :param vselect : For plotting take 1/vselect vector in x axis and 1/vselect vector in y-axis. Could make the plot
        more readable
        :return: fig and ax
        """
        from modules.global_variable.param import plot_param
        frame_num = frame
        # Get the frame to plot
        if type(frame) == int:
            try:
                frame = self[frame]
            except:
                raise Exception("Specified frame number is out of range, deleted or not loaded")
        else:
            try:
                frame = self.get_frame_time(frame)
            except:
                raise Exception("Specified time is out of range, or no frame are loaded")

        fig, ax = plt.subplots(1, 1)

        # plot flood
        if flood in self.get_header():

            toplot = frame[flood].reshape(frame.mesh_dim[1], frame.mesh_dim[0])

            if cb_scale:
                img = ax.imshow(toplot, extent=self.extent, cmap=plot_param["cmap"], origin="lower", vmin=cb_scale[0]
                                , vmax=cb_scale[1])
                delta = (cb_scale[1] - cb_scale[0]) / 10
                ticks = [cb_scale[0] + delta * i for i in range(11)]
                cb = fig.colorbar(img, ticks=ticks)
                cb.set_label(flood)
                ticks = ["{0:.6g}".format(cb_scale[0] + delta * i) for i in range(11)]
                cb.ax.set_yticklabels(ticks)
            else:
                img = ax.imshow(toplot, extent=self.extent, cmap=plot_param["cmap"], origin="lower")
                cb = fig.colorbar(img)
                cb.set_label(flood)
                # scatter
        if scatter:
            try:
                x = frame[scatter[0]].reshape(frame.mesh_dim[0], frame.mesh_dim[1])
                y = frame[scatter[1]].reshape(frame.mesh_dim[0], frame.mesh_dim[1])
                scat = ax.scatter(x, y, s=1)
            except:
                scat = ax.scatter(scatter[0], scatter[1], s=1)

        # plot vector
        if vector:
            if vselect != None:
                vx = self.get_grid_data(var_name=vector[0], frame=frame_num)
                vy = self.get_grid_data(var_name=vector[1], frame=frame_num)
                x = self.get_grid_data(var_name=self.x_label, frame=frame_num)
                y = self.get_grid_data(var_name=self.y_label, frame=frame_num)

                sel1 = np.arange(0, vx.shape[0], vselect - 1)
                vx = np.take(vx, sel1, axis=0)
                vy = np.take(vy, sel1, axis=0)
                x = np.take(x, sel1, axis=0)
                y = np.take(y, sel1, axis=0)

                sel1 = np.arange(0, vx.shape[1], vselect - 1)
                vx = np.take(vx, sel1, axis=1)
                vy = np.take(vy, sel1, axis=1)
                x = np.take(x, sel1, axis=1)
                y = np.take(y, sel1, axis=1)

                ax.quiver(x, y, vx, vy, scale_units="xy", scale=vscale, width=plot_param["vector_linewidths"])
            else:
                vx = frame[vector[0]]
                vy = frame[vector[1]]
                ax.quiver(frame[self.x_label], frame[self.y_label], vx, vy, scale_units="xy", scale=vscale)

        # mesh
        if mesh:
            set_x = list(set(frame[self.x_label] - self.dx / 2.0))
            set_y = list(set(frame[self.y_label] - self.dy / 2.0))
            x, y = np.meshgrid(set_x, set_y)

            # plt.scatter(x, y)

            segs1 = np.stack((x, y), axis=2)
            segs2 = segs1.transpose(1, 0, 2)
            plt.gca().add_collection(LineCollection(segs1, colors="k"))
            plt.gca().add_collection(LineCollection(segs2, colors="k"))

        # plot lines
        if lines:
            if not lines_levels:
                lines_levels = [0] * len(lines)  # Default value is 0
            k = 0
            labels = []
            color_set = ['k', 'tab:gray', 'tab:blue']
            for line in lines:
                line_to_plot = frame[line].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                ct = ax.contour(line_to_plot, levels=lines_levels[k], linewidths=plot_param["linewidths"],
                                linestyles=plot_param["linestyles"], zorder=plot_param["zorder"],
                                extent=self.extent,
                                colors=color_set[k])
                labels.append(mpatches.Patch(color=color_set[k], label=line))

                if not type(lines_levels[k]) == int:  # disp line value on the graph if not default value
                    plt.clabel(ct, inline=1, fontsize=10)

                k += 1
            plt.legend(handles=labels, loc="lower center")

        # plot iso_lines
        if iso_lines:
            for line in iso_lines:
                line_to_plot = frame[line].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                ct = ax.contour(line_to_plot, linewidths=plot_param["linewidths"],
                                linestyles=plot_param["linestyles"], zorder=plot_param["zorder"],
                                extent=self.extent)
            plt.clabel(ct, inline=1, fontsize=10)

        # display simulation time
        if disp_time:
            x_text = self.extent[0]
            y_text = self.extent[3] * 1.1
            text = "Time = " + str(frame.time) + " s"
            ax.text(x_text, y_text, text)
        if title != '':
            plt.title(title)
        # Put labels
        ax.set_xlabel(self.x_label + " [m]")
        ax.set_ylabel(self.y_label + " [m]")

        plt.axis('equal')
        plt.gca().set_aspect('equal', adjustable='box')
        ax.legend(loc="lower center")
        if zoom != None:
            plt.xlim(zoom[0])
            plt.ylim(zoom[1])

        if show:
            plt.show()
        return fig, ax

    def plot_3D(self, frame=1, flood='', cb_scale=[], vector=[], lines=[], lines_levels=[], vscale=0.1, scatter=[],
                mesh=False,
                iso_lines=[], disp_time=False, show=True, title='', zoom=None, vselect=None):
        """
        a quick integrated plot function to quick plot values for 2D
        :param show: show or not the plot
        :param disp_time: disp simulation time on the plot
        :param cb_scale: color bar scale for flood plots
        :param frame: frame number
        :param flood: flood field (i.e with color map such as temperature)
        :param vector: [vx,vy], list of the name of the x component and y component of the vector. vx and vy are string
        which are in the header
        :param lines: plot lines from a field (by default plot for the isovalues 0). Should be a list of string
        :param lines_levels: list the wanted lines levels
        :param vscale: scale for the arrow of the vector (to have a good view)
        :param scatter: data to scatter
        :param mesh: if true, plot the mesh
        :param iso_lines: name of isolines to plot
        :param title: add a title to a plot
        :param zoom: should be [(xmin,xmax),(ymin,ymax)] to zoom on the figure
        :param vselect : For plotting take 1/vselect vector in x axis and 1/vselect vector in y-axis. Could make the plot
        more readable
        :return: fig and ax
        """
        from modules.global_variable.param import plot_param
        frame_num = frame
        # Get the frame to plot
        if type(frame) == int:
            try:
                frame = self[frame]
            except:
                raise Exception("Specified frame number is out of range, deleted or not loaded")
        else:
            try:
                frame = self.get_frame_time(frame)
            except:
                raise Exception("Specified time is out of range, or no frame are loaded")

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        # plot flood
        if flood in self.get_header():

            toplot = frame[flood].reshape(frame.mesh_dim[1], frame.mesh_dim[0])

            if cb_scale:
                img = ax.imshow(toplot, extent=self.extent, cmap=plot_param["cmap"], origin="lower", vmin=cb_scale[0]
                                , vmax=cb_scale[1])
                delta = (cb_scale[1] - cb_scale[0]) / 10
                ticks = [cb_scale[0] + delta * i for i in range(11)]
                cb = fig.colorbar(img, ticks=ticks)
                cb.set_label(flood)
                ticks = ["{0:.6g}".format(cb_scale[0] + delta * i) for i in range(11)]
                cb.ax.set_yticklabels(ticks)
            else:
                img = ax.imshow(toplot, extent=self.extent, cmap=plot_param["cmap"], origin="lower")
                cb = fig.colorbar(img)
                cb.set_label(flood)
                # scatter
                if scatter:
                    try:
                        x = frame[scatter[0]].reshape(frame.mesh_dim[0], frame.mesh_dim[1])
                        y = frame[scatter[1]].reshape(frame.mesh_dim[0], frame.mesh_dim[1])
                        scat = ax.scatter(x, y, s=1)
                    except:
                        scat = ax.scatter(scatter[0], scatter[1], s=1)

                # plot vector
                if vector:
                    if vselect != None:
                        vx = self.get_grid_data(var_name=vector[0], frame=frame_num)
                        vy = self.get_grid_data(var_name=vector[1], frame=frame_num)
                        x = self.get_grid_data(var_name=self.x_label, frame=frame_num)
                        y = self.get_grid_data(var_name=self.y_label, frame=frame_num)

                        sel1 = np.arange(0, vx.shape[0], vselect-1)
                        vx = np.take(vx, sel1, axis=0)
                        vy = np.take(vy, sel1, axis=0)
                        x = np.take(x, sel1, axis=0)
                        y = np.take(y, sel1, axis=0)

                        sel1 = np.arange(0, vx.shape[1], vselect-1)
                        vx = np.take(vx, sel1, axis=1)
                        vy = np.take(vy, sel1, axis=1)
                        x = np.take(x, sel1, axis=1)
                        y = np.take(y, sel1, axis=1)

                        ax.quiver(x, y, vx, vy, scale_units="xy", scale=vscale)
                    else:
                        vx = frame[vector[0]]
                        vy = frame[vector[1]]
                        ax.quiver(frame[self.x_label], frame[self.y_label], vx, vy, scale_units="xy", scale=vscale)

                # mesh
                if mesh:
                    set_x = list(set(frame[self.x_label] - self.dx / 2.0))
                    set_y = list(set(frame[self.y_label] - self.dy / 2.0))
                    x, y = np.meshgrid(set_x, set_y)

                    # plt.scatter(x, y)

                    segs1 = np.stack((x, y), axis=2)
                    segs2 = segs1.transpose(1, 0, 2)
                    plt.gca().add_collection(LineCollection(segs1, colors="k"))
                    plt.gca().add_collection(LineCollection(segs2, colors="k"))

                # plot lines
                if lines:
                    if not lines_levels:
                        lines_levels = [0] * len(lines)  # Default value is 0
                    k = 0
                    labels = []
                    color_set = ['k', 'tab:gray', 'tab:blue']
                    for line in lines:
                        line_to_plot = frame[line].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                        ct = ax.contour(line_to_plot, levels=lines_levels[k], linewidths=plot_param["linewidths"],
                                        linestyles=plot_param["linestyles"], zorder=plot_param["zorder"],
                                        extent=self.extent,
                                        colors=color_set[k])
                        labels.append(mpatches.Patch(color=color_set[k], label=line))

                        if not type(lines_levels[k]) == int:  # disp line value on the graph if not default value
                            plt.clabel(ct, inline=1, fontsize=10)

                        k += 1
                    plt.legend(handles=labels, loc="lower center")

                # plot iso_lines
                if iso_lines:
                    for line in iso_lines:
                        line_to_plot = frame[line].reshape(frame.mesh_dim[1], frame.mesh_dim[0])
                        ct = ax.contour(line_to_plot, linewidths=plot_param["linewidths"],
                                        linestyles=plot_param["linestyles"], zorder=plot_param["zorder"],
                                        extent=self.extent)
                    plt.clabel(ct, inline=1, fontsize=10)

                # display simulation time
                if disp_time:
                    x_text = self.extent[0]
                    y_text = self.extent[3] * 1.1
                    text = "Time = " + str(frame.time) + " s"
                    ax.text(x_text, y_text, text)
                if title != '':
                    plt.title(title)
                # Put labels
                ax.set_xlabel(self.x_label + " [m]")
                ax.set_ylabel(self.y_label + " [m]")

            plt.axis('equal')
            plt.gca().set_aspect('equal', adjustable='box')
            ax.legend(loc="lower center")
            if zoom != None:
                plt.xlim(zoom[0])
                plt.ylim(zoom[1])

            if show:
                plt.show()
            return fig, ax

    # Filter data option
    def limiter(self, frame, var_name, mini=None, maxi=None):
        """
        :param maxi: maximum value for the limiter
        :param mini: minimum value for the limiter
        :param frame: frame number
        :param var_name: variable name
        :return: None, but modify the var_name, by limiting up and down values
        """
        if mini is None:
            mini = min(self[frame][var_name])
        if maxi is None:
            maxi = max(self[frame][var_name])
        data = np.array(self[frame][var_name])
        data[data > maxi] = maxi
        data[data < mini] = mini
        self[frame][var_name] = data

    # write file
    def write_csv(self, frame, filename, sep=";"):
        """
        Write all the data from a frame in a csv file
        :param frame: frame number
        :param filename: the written filename
        :param sep: column separator
        :return: None
        """
        self[frame].data.to_csv(filename, sep=sep)

    def write_pickle(self, filename):
        """
        Wrtie data into a pickle binary file.
        :param frame: number of the frame that would be save
        :param filename: filename
        :return: None
        """
        import pickle as pk
        pk.dump(self, open(filename, "wb"))

    # Open file
    def open_pickle(self, filename):
        """
        Open a .pickle binary file containing a Tectplot class and return it.
        :param filename: path and filename of the .pickle file
        :return: None
        """
        import pickle as pk
        return pk.load(open(filename, 'rb'))

    # __*__ Operator definition
    def __getitem__(self, framenumber):
        """
        Return a plt_obj
        :param framenumber: the frame number
        :return: plt_obj
        """
        return self.frames[framenumber]

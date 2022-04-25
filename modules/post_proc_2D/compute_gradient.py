import numpy as np


def old_compute_gradient(Tecplot_obj, frame, var_name):
    """
    Compute the 2D gradient of a field
    :param Tecplot_obj: a Tecplot_obj
    :param frame: the frame number to compute gradient
    :param var_name: variable name to compute gradient
    :return: X and Y coordinate of the gradient
    """
    var = np.array(Tecplot_obj[frame][var_name])
    var = var.reshape(Tecplot_obj[frame].mesh_dim[1], Tecplot_obj[1].mesh_dim[0])
    dy = Tecplot_obj.dy.reshape(Tecplot_obj[frame].mesh_dim[1], Tecplot_obj[frame].mesh_dim[0])
    dx = Tecplot_obj.dy.reshape(Tecplot_obj[frame].mesh_dim[1], Tecplot_obj[frame].mesh_dim[0])
    grad = np.array(np.gradient(var))
    nx = (grad[0] / dx).reshape(Tecplot_obj[frame].mesh_dim[1] * Tecplot_obj[frame].mesh_dim[0])
    ny = (grad[1] / dy).reshape(Tecplot_obj[frame].mesh_dim[1] * Tecplot_obj[frame].mesh_dim[0])
    Tecplot_obj[frame]["\/" + var_name + "_y"] = nx
    Tecplot_obj[frame]["\/" + var_name + "_x"] = ny


def compute_gradient(Tecplot_obj, frame, var_name):
    """
    Compute the 2D gradient of a field
    :param Tecplot_obj: a Tecplot_obj
    :param frame: the frame number to compute gradient
    :param var_name: variable name to compute gradient
    :return: X and Y coordinate of the gradient
    """

    var = Tecplot_obj.get_grid_data(frame=frame, var_name=var_name)
    dy = Tecplot_obj.get_grid_data(frame=frame, var_name="dy")
    dx = Tecplot_obj.get_grid_data(frame=frame, var_name="dx")


    # comput the gradient along the axis = 1, i.e it's the x compnent
    nx = np.gradient(var, axis=1) / dx
    ny = np.gradient(var, axis=0) / dy

    nx = nx.reshape(nx.size)
    ny = ny.reshape(ny.size)

    Tecplot_obj[frame]["\/" + var_name + "_y"] = ny
    Tecplot_obj[frame]["\/" + var_name + "_x"] = nx

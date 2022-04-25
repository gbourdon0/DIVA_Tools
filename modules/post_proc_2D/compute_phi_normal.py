import numpy as np
import modules.global_variable.global_variable as gv


def old_phi_normal(Tecplot_obj, frame, phi_name="Phi"):
    """
    :param phi_name: name of the field to compute normal
    :param frame: frame number of the Tecplot_obj
    :param Tecplot_obj:
    :return: normal vector field of phi
    """
    # Tecplot_obj.plot( frame=1, flood='Temperature',vector = ["U_r","U_z"], lines=["Phi"], lines_levels=[],vscale =1000)
    phi = np.array(Tecplot_obj[frame][phi_name])
    phi = phi.reshape(Tecplot_obj[frame].mesh_dim[1], Tecplot_obj[frame].mesh_dim[0])

    dy = Tecplot_obj.dx.reshape(Tecplot_obj[frame].mesh_dim[1], Tecplot_obj[frame].mesh_dim[0])
    dx = Tecplot_obj.dy.reshape(Tecplot_obj[frame].mesh_dim[1], Tecplot_obj[frame].mesh_dim[0])
    nx, ny = [], []
    for i in range(Tecplot_obj[frame].mesh_dim[1]):
        for j in range(Tecplot_obj[frame].mesh_dim[0]):
            if i == Tecplot_obj[frame].mesh_dim[1] - 1 or j == Tecplot_obj[frame].mesh_dim[0] - 1:
                nx.append(np.nan)
                ny.append(np.nan)
            elif i == Tecplot_obj[frame].mesh_dim[1] or j == Tecplot_obj[frame].mesh_dim[0]:
                nx.append(np.nan)
                ny.append(np.nan)
            else:
                dxphi = (phi[i + 1, j] - phi[i - 1, j]) / (dx[i, 1] + dx[i - 1, 1])
                dyphi = (phi[i, j + 1] - phi[i, j - 1]) / (dy[1, j] + dy[1, j - 1])
                norm_n_solid = np.sqrt(dxphi * dxphi + dyphi * dyphi)
                try:
                    nx.append(dxphi / norm_n_solid)
                    ny.append(dyphi / norm_n_solid)
                except:
                    nx.append(np.nan)
                    ny.append(np.nan)
    # J'ai inverse les coordonnes dans le calcul, donc on fait l'affectation inverse, oupsi
    Tecplot_obj[frame][phi_name + "_ny"] = nx
    Tecplot_obj[frame][phi_name + "_nx"] = ny
    return Tecplot_obj


def phi_normal(Tecplot_obj, frame, phi_name="Phi"):
    """
    :param phi_name: name of the field to compute normal
    :param frame: frame number of the Tecplot_obj
    :param Tecplot_obj:
    :return: normal vector field of phi
    """

    phi = Tecplot_obj.get_grid_data(frame = frame, var_name = phi_name)
    dx = Tecplot_obj.get_grid_data(frame = frame, var_name = "dx")
    dy = Tecplot_obj.get_grid_data(frame = frame, var_name = "dy")


    # Calcul le long de l'axis 1 --> grad selon x
    nx = np.gradient(phi, axis = 1)/dx
    ny = np.gradient(phi, axis = 0)/dy
    norm = np.sqrt(nx**2+ny**2)

    nx = nx/norm
    ny = ny/norm

    nx = nx.reshape(nx.size)
    ny = ny.reshape(ny.size)


    Tecplot_obj[frame][phi_name + "_ny"] = ny
    Tecplot_obj[frame][phi_name + "_nx"] = nx
    return Tecplot_obj

import os
from modules.data_reader.Tecplot import Tecplot
import numpy as np
from numpy import linalg as LA
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import matplotlib.pyplot as plt
from modules.data_reader.pickle_reader import PickleReader as pr
import modules.diva_input as DIVA_in
from scipy import constants
import modules.diva_input as DIVA

diva_input = DIVA.diva_input()
import pandas as pd

paf = "/home/gbourdon/03_DIVA_dev/000_BENCHMARK/05_conv_nat_benchmark"
configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/images")
filename = "anim015.plt"
diva_input.load(paf + "/run")
data = Tecplot()
data.add_frame(paf + "/animation_files/" + filename)
print(data.get_header())

# Compute gradient

grad = np.gradient(data.get_grid_data(frame=1, var_name="Tghost_immersed_sol"))
dy = data.dy.reshape(data[1].mesh_dim[0], data[1].mesh_dim[1])
dx = data.dx.reshape(data[1].mesh_dim[0], data[1].mesh_dim[1])
grad_x = grad[0] / dx
grad_y = grad[1] / dy
thermal_flux = - diva_input.TP.kth_vap * (grad_x ** 2 + grad_y ** 2) ** .5
data.add_grid_to_frame(frame=1, var_name="Heat Flux", grid=thermal_flux)
data.add_grid_to_frame(frame=1, var_name="Heat Flux_x", grid=- diva_input.TP.kth_vap * grad_x)
data.add_grid_to_frame(frame=1, var_name="Heat Flux_y", grid=- diva_input.TP.kth_vap * grad_y)

# Compute phi_normal

grad_phi = np.gradient(data.get_grid_data(frame=1, var_name="phi_solid"))
dy = data.dy.reshape(data[1].mesh_dim[0], data[1].mesh_dim[1])
dx = data.dx.reshape(data[1].mesh_dim[0], data[1].mesh_dim[1])
grad_phi_x = grad_phi[0] / dx
grad_phi_y = grad_phi[1] / dy
norm_grad = (grad_phi_x**2+grad_phi_y**2)**.5
data.add_grid_to_frame(frame=1, var_name="phi_solid_nx", grid=grad_phi_x/norm_grad)
data.add_grid_to_frame(frame=1, var_name="phi_solid_ny", grid=grad_phi_y/norm_grad)
#data.plot(flood = "Temperature", vector=["phi_solid_nx","phi_solid_ny"], vscale = 5e2, lines = ["phi_solid"])

# Compute norm heat flux
hf = data[1]["Heat Flux_x"]*data[1]["phi_solid_nx"]+data[1]["Heat Flux_y"]*data[1]["phi_solid_ny"]
data.add_grid_to_frame(frame = 1, var_name = "Heat Flux", grid = hf )

import copy
data2 = copy.deepcopy(data)
def phi_normal(Tecplot_obj, frame, phi_name="Phi"):
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

def gradient(Tecplot_obj, frame, phi_name=""):
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
                nx.append(dxphi)
                ny.append(dyphi)

    # J'ai inverse les coordonnes dans le calcul, donc on fait l'affectation inverse, oupsi
    Tecplot_obj[frame]["\/"+phi_name + "_ny"] = nx
    Tecplot_obj[frame]["\/"+phi_name + "_nx"] = ny
    return Tecplot_obj

print("gradient")
gradient(data2,frame = 1, phi_name ="Tghost_immersed_sol")
print("normal")
phi_normal(data2,frame = 1, phi_name = "phi_solid")

Heat_Flux = - diva_input.TP.kth_vap * (data2[1]["\/Tghost_immersed_sol_ny"]*data2[1]["phi_solid_ny"]+data2[1]["\/Tghost_immersed_sol_nx"]*data2[1]["phi_solid_nx"])
data2.add_variable_to_frame(frame = 1, var_name = "Heat Flux", var = Heat_Flux)


def angle_of_vectors(a, b):
    """
    Compute angle between vector a and b for 2D vector
    :param a: should be a size 2 list
    :param b: should be a size 2 list
    :return: angle in degree
    """
    import numpy as np
    import numpy.linalg as LA

    inner = np.inner(a, b)
    norms = LA.norm(a) * LA.norm(b)
    if norms == 0.0:
        return None
    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    deg = np.rad2deg(rad)
    return deg


def angular_wall_heat_flux(Tecplot_obj, frame, phi_sol_name):
    """
    Compute the angular heat flux from gas to liquid (without the evaporation rate)
    :param phi_sol_name: name of the phi function for the IMB
    :param Tecplot_obj: tecplot_obj as defined in data_reader/Tecplot
    :param frame: frame number (or .plt number) for the Tecplot_obj
    :return:angle list and associated heat flux
    """
    xx, yy = Tecplot_obj.get_iso_value_2D(frame=1, var_name=phi_sol_name, iso_values=[0])
    x, y = Tecplot_obj[frame][Tecplot_obj.x_label], Tecplot_obj[frame][Tecplot_obj.y_label]
    from modules.post_proc_2D.interp2D import interp2D
    FLUX = interp2D(np.array(Tecplot_obj[frame]["Heat Flux"]), x, y, xx, yy, resolve_nan = True,kind = 'cubic')
    theta2 = np.array([angle_of_vectors([0, -1], [xx[i], yy[i]]) for i in range(len(xx))])
    return theta2[2:-2], FLUX[2:-2]  # To remove first and last value of angle which are inconsitent due to derivative
print("go")
theta,flux = angular_wall_heat_flux(data,frame = 1, phi_sol_name= "phi_solid")
print("go2")
theta2,flux2 = angular_wall_heat_flux(data2,frame = 1, phi_sol_name= "phi_solid")
plt.plot(theta,-flux, label = "numpy")
plt.plot(theta2,-flux2, label = "a la mano")
plt.legend()
plt.show()
import numpy as np
import pandas as pd
import os
import modules.post_proc_2D as pt
import modules.diva_input as DIVA_in
from modules.data_reader.Tecplot import Tecplot
import matplotlib.pyplot as plt
from modules.VideoMaker.MPLVideoMaker import MPLVideoMaker

paf = "/home/gbourdon/02_DIVA_benchmark_drag/13_0"
try:
    os.mkdir(paf+"/post_traitement/video/")
except:
    pass
import numpy as np
import pandas as pd
import os
import modules.post_proc_2D as pt
import modules.diva_input as DIVA_in
from modules.data_reader.Tecplot import Tecplot
import matplotlib.pyplot as plt
from modules.VideoMaker.MPLVideoMaker import MPLVideoMaker

paf = "/home/gbourdon/02_DIVA_benchmark_drag/13_0"
try:
    os.mkdir(paf+"/post_traitement/video/")
except:
    pass
video_name = paf + "/post_traitement/video/Temperature_2.mp4"
fps = 24
filelist = os.listdir(paf + "/animation_files")
filelist.sort()
filelist = filelist[49:50]
DIVA_plt = Tecplot()
video = MPLVideoMaker()
print("Import .plt files")

for plt_file in filelist:
    DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)


#DIVA_plt.from_axi_to_2D()
frame_nb = 1
phi_sol = DIVA_plt[1]["Phi_solid"]
R = DIVA_plt[1]["R"]
Z = DIVA_plt[1]["Z"]
DIVA_plt[1]["Theta"] = len(Z)*[0] #Init Theta axe
Theta = DIVA_plt[1]["Theta"]
rot = [90,180,270]

phi_sol = phi_sol.reshape(512,1024,1)
R = R.reshape(512,1024,1)
Z = Z.reshape(512,1024,1)
Theta = Theta.reshape(512,1024,1)

phi_plot = phi_sol
R_plot = R
Z_plot = Z
Theta_plot = Theta
for angle in rot:
    new_phi = phi_sol
    new_R = R*np.cos(np.deg2rad(angle))
    new_Z = Z
    new_Theta = R*np.sin(np.deg2rad(angle))

    phi_plot = np.concatenate((phi_plot,new_phi), axis=2 )
    R_plot = np.concatenate((R_plot,new_R), axis=2 )
    Z_plot = np.concatenate((Z_plot,new_Z), axis=2 )
    Theta_plot = np.concatenate((Theta_plot,new_Theta), axis=2 )
import matplotlib.pyplot as plt

print(R_plot.shape)
print(Z_plot.shape)
print(phi_plot.shape)
print(phi_plot.min())


import pyvista as pv

#%% Data
grid = pv.StructuredGrid(R, Z, Theta)
grid["vol"] = phi_sol.flatten()
contours = grid.contour([0])

#%% Visualization
pv.set_plot_theme('document')
p = pv.Plotter()
p.add_mesh(contours, scalars=contours.points[:, 2], show_scalar_bar=False)
p.show()









'''fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(R_plot[:,:,0], Z_plot[:,:,0], Theta_plot[:,:,0], c=phi_plot[:,:,0],alpha=0.7, marker='.')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D contour')
plt.show()'''
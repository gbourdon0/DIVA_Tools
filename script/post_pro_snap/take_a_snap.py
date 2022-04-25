import os
from modules.data_reader.Tecplot import Tecplot
from multiprocessing import Process
import multiprocessing
import numpy as np
from modules.VideoMaker.MPLVideoMaker import MPLVideoMaker

#paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
#paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
#paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1"

DIVA_plt = Tecplot()
DIVA_plt.add_frame("/work/gbourdon/02_benchmark_FC72/11_5d-1/animation_files//anim190.plt")
DIVA_plt.select_data_range((-0.01,0.01),(-0.01,0.01))
print(DIVA_plt[1].time)

vel = np.sqrt(DIVA_plt[DIVA_plt.nb_frames]["U_r"]**2+DIVA_plt[DIVA_plt.nb_frames]["U_z"]**2)
DIVA_plt.add_variable_to_frame(frame = DIVA_plt.nb_frames, var_name="Velocity (m/s)", var = vel)
fig, ax = DIVA_plt.plot(frame=DIVA_plt.nb_frames, flood="Velocity (m/s)", lines=["Phi", "Phi_solid"], disp_time=True,
                                show=True,
                                cb_scale=[0, 1.5,6], vector=["U_r", "U_z"], vscale = 5e3)
import os
from modules.data_reader.Tecplot import Tecplot
from multiprocessing import Process
import multiprocessing

from modules.VideoMaker.MPLVideoMaker import MPLVideoMaker


paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1"
title = "v = 0.5 m/s"
try:
    os.mkdir(paf + "/post_traitement/video/")
except:
    pass

video_name = paf + "/post_traitement/video/Temperature_2.mp4"
fps = 24
filelist = os.listdir(paf + "/animation_files")
filelist = [files for files in filelist if ".plt" in files]
filelist = filelist[150:151]
filelist.sort()
DIVA_plt = Tecplot()
DIVA_plt.add_frame(paf + "/animation_files/" + filelist[0])

DIVA_plt.from_axi_to_2D()

ig, ax = DIVA_plt.plot(frame=1, lines=["Phi", "Phi_solid"], disp_time=True,
                                show=True,
                                cb_scale=[310, 560], title = title)
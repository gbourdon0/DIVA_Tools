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

paf = "/work/gbourdon/02_benchmark_FC72/13_0"
try:
    os.mkdir(paf+"/post_traitement/video/")
except:
    pass
video_name = paf + "/post_traitement/video/Temperature_2.mp4"
fps = 24
filelist = os.listdir(paf + "/animation_files")
filelist = [files for files in filelist if ".plt" in files]
filelist.sort()
DIVA_plt = Tecplot()
video = MPLVideoMaker()
print("Import .plt files")

for plt_file in filelist:
    DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)

print("Transform to 2D")
DIVA_plt.from_axi_to_2D()
frame_nb = 1
print("Building video")
for plt_file in filelist:

    # Building frame
    fig, ax = DIVA_plt.plot(frame=frame_nb, flood="Temperature", lines=["Phi", "Phi_solid"], disp_time=True, show=False,cb_scale=[310,560])
    if video.init == False:
        video.init_video(video_name,fig,fps = fps)
    video.add_frame(fig)
    frame_nb +=1
print("Writing video")
video.write_video()


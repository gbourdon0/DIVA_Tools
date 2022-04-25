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
title = "v = 0.5 m/s"
try:
    os.mkdir(paf + "/post_traitement/video/")
except:
    pass

video_name = paf + "/post_traitement/video/Temperature_2_zoom.mp4"
fps = 24
filelist = os.listdir(paf + "/animation_files")
filelist = [files for files in filelist if ".plt" in files]
filelist.sort()
filelist = filelist[156:157]
DIVA_plt = Tecplot()
video = MPLVideoMaker()
print("Import .plt files")

manager = multiprocessing.Manager()
fig_list = manager.list(range(len(filelist)))


def load_and_build_fig(files, n_start):
    for plt_file in files:
        DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)

        vel = np.sqrt(DIVA_plt[DIVA_plt.nb_frames]["U_r"]**2+DIVA_plt[DIVA_plt.nb_frames]["U_z"]**2)
        DIVA_plt.add_variable_to_frame(frame = DIVA_plt.nb_frames, var_name="Velocity (m/s)", var = vel)

    print("Transform to 2D")
    #To zoom or not
    DIVA_plt.select_data_range((-0.01,0.01),(-0.01,0.01))
    DIVA_plt.from_axi_to_2D()
    print(DIVA_plt.x_label)
    frame_nb = 1
    print("Building figures")
    k = n_start
    for plt_file in files:
        print(k)
        fig, ax = DIVA_plt.plot(frame=frame_nb, flood="Velocity (m/s)", lines=["Phi", "Phi_solid"], disp_time=True,
                                show=True,
                                cb_scale=[0, 1.5], title = title, vector=["U_r", "U_z"], vscale = 8e2, vselect = 20)
        fig_list[k] = fig
        frame_nb += 1
        k += 1


nb_proc = 8
N = len(filelist) // nb_proc
p1 = Process(target=load_and_build_fig, args=(filelist[:N], 0))
p2 = Process(target=load_and_build_fig, args=(filelist[N:2 * N], N))
p3 = Process(target=load_and_build_fig, args=(filelist[2 * N:3 * N], 2 * N))
p4 = Process(target=load_and_build_fig, args=(filelist[3 * N:4 * N], 3 * N))
p5 = Process(target=load_and_build_fig, args=(filelist[4 * N:5 * N], 4 * N))
p6 = Process(target=load_and_build_fig, args=(filelist[5 * N:6 * N], 5 * N))
p7 = Process(target=load_and_build_fig, args=(filelist[6 * N:7 * N], 6 * N))
p8 = Process(target=load_and_build_fig, args=(filelist[7 * N:], 7 * N))

p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()
p7.start()
p8.start()

p1.join()
p2.join()
p3.join()
p4.join()
p5.join()
p6.join()
p7.join()
p8.join()

print("Building video")
k = 0
for fig in fig_list:
    if video.init == False:
        video.init_video(video_name, fig, fps=fps)
    video.add_frame(fig)
    print(f"frame {k} built.")
    k += 1
print("Writing video")
video.write_video()

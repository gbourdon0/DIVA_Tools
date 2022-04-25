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
filelist.sort()
DIVA_plt = Tecplot()
video = MPLVideoMaker()
print("Import .plt files")

manager = multiprocessing.Manager()
fig_list = manager.list(range(len(filelist)))


def load_and_build_fig(files, n_start):
    for plt_file in files:
        DIVA_plt.add_frame(paf + "/animation_files/" + plt_file)

    print("Transform to 2D")
    DIVA_plt.from_axi_to_2D()

    frame_nb = 1
    print("Building figures")
    k = n_start
    for plt_file in files:
        fig, ax = DIVA_plt.plot(frame=frame_nb, flood="Temperature", lines=["Phi", "Phi_solid"], disp_time=True,
                                show=False,
                                cb_scale=[310, 560], title = title)
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
    k += 1
print("Writing video")
video.write_video()

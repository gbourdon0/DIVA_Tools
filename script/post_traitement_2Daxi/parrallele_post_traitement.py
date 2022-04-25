"""# This is a sample Python script.
Post process a whole DIVA simulation for 2D axi sphere IMB.
This is done in parrallele to save time
"""

import modules.global_variable.global_variable as gv
from modules.data_reader import read_dat
from multiprocessing import Process
from script.post_traitement_2Daxi.pt_sphere import pt_sphere
import os
from modules.data_reader.Tecplot import Tecplot
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    paf = "/work/gbourdon/02_benchmark_FC72/13_0"
    #paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
    #paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
    #paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
    #paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
    #paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"
    filelist = os.listdir(paf + "/animation_files")
    filelist.sort()


    # Post-treatment 1D
    def f1(liste):
        for plt_name in liste:
            pt_sphere(paf, plt_name, debug=False)


    nb_proc = 8
    N = len(filelist) // nb_proc
    p1 = Process(target=f1, args=(filelist[:N],))
    p2 = Process(target=f1, args=(filelist[N:2 * N],))
    p3 = Process(target=f1, args=(filelist[2 * N:3 * N],))
    p4 = Process(target=f1, args=(filelist[3 * N:4 * N],))
    p5 = Process(target=f1, args=(filelist[4 * N:5 * N],))
    p6 = Process(target=f1, args=(filelist[5 * N:6 * N],))
    p7 = Process(target=f1, args=(filelist[6 * N:7 * N],))
    p8 = Process(target=f1, args=(filelist[7 * N:],))

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

    # Data 0D
    gv.DIVA_input.load(paf + "/run")
    gv.data_0D = read_dat(paf + "/run/Data/Heat_flux.dat")
    h_wg = gv.data_0D["Wall_heat_flux"] / (gv.DIVA_input.IC.T_immersed - gv.DIVA_input.TP.t_sat)
    Nu_wg = h_wg * gv.DIVA_input.IC.solid_obj_dim[0] / gv.DIVA_input.TP.kth_vap
    gv.data_0D["h_wg"] = h_wg
    gv.data_0D["Nu_wg"] = Nu_wg

    gv.data_0D.to_pickle(paf + "/post_traitement/data_0D.pickle")

    # Write time liste

    files = os.listdir(paf + "/animation_files")
    files.sort()
    files = [paf + "/animation_files/" + f for f in files]

    hey = Tecplot()
    hey.add_frame_list(files)
    t = []

    for i in range(1, hey.nb_frames + 1):
        t.append(hey[i].time)

    df = pd.DataFrame()
    df["time (s)"] = t
    df.to_csv(paf + "/post_traitement/time.csv", sep=";")

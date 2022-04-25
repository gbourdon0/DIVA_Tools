from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import seaborn as sns
import modules.analytique_solutions.sphere as sp
import pandas as pd
import modules.diva_input as DIVA_in

# paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
# paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"
# paf = "/work/gbourdon/02_benchmark_FC72/07_2d-1/"
# paf = "/work/gbourdon/02_benchmark_FC72/08_3d-1/"
# paf = "/work/gbourdon/02_benchmark_FC72/09_4d-1/"
# paf = "/work/gbourdon/02_benchmark_FC72/11_5d-1/"


# ***************************** Film thickness -  full
theta_max = 170
plt_min = 170


def film_tchikness(data_1D, DIVA_input, time, theta_max):
    bbox = dict(boxstyle="round", fc="1")
    plt_min = data_1D.time2plt(time)
    # plot fig
    fig, (ax1, ax2) = plt.subplots(1, 2)
    set_size(subplots=(1, 2))
    convergence = []  # check convergence
    # Comme on est a l'interface, pour chaque plt, il n'y  a pas forcement le meme nombre de point suivant l'angle (
    # suivant comment evolue l'interface. On resample donc toutes les donnees avec un pas de temps de 1 deg

    mean = np.zeros(theta_max - 2)
    std = np.zeros(theta_max - 2)
    theta = np.arange(2, theta_max, 1)
    N = 0
    for i in range(0, len(data_1D.key_list)):
        df = data_1D[data_1D.key_list[i]].loc[data_1D[data_1D.key_list[i]]["theta_interface"] < theta_max]

        f1 = interp1d(df["theta_interface"], df["Film thickness"],
                      kind='linear', fill_value="extrapolate")
        if i < len(data_1D.key_list) - 1:
            df2 = data_1D[data_1D.key_list[i + 1]].loc[data_1D[data_1D.key_list[i + 1]]["theta_interface"] < theta_max]
            f2 = interp1d(df2["theta_interface"],
                          df2["Film thickness"], kind='linear', fill_value="extrapolate")
        try:
            diff = sum(abs(f1(theta) - f2(theta))) / sum(abs(f1(theta)))
        except:
            diff = np.nan  # in case
        convergence.append(diff)
        if i >= plt_min:
            N += 1
            mean += f1(theta)

    mean = mean / N
    # Compute std
    for i in range(len(data_1D.key_list) - N, len(data_1D.key_list)):
        df = data_1D[data_1D.key_list[i]].loc[data_1D[data_1D.key_list[i]]["theta_interface"] < theta_max]
        f1 = interp1d(df["theta_interface"], df["Film thickness"],
                      kind='linear', fill_value="extrapolate")
        std += (f1(theta) - mean) ** 2
    std = np.sqrt(std / N)
    # Solution theorique sans soufflage

    theorique = np.array([sp.film_tchikness(DIVA_input, D=10e-3, theta=angle, dtheta=0.1) for angle in theta])

    plt.subplot(1, 2, 1)
    plt.title("Film thickness")
    lab = r"\begin{flushleft} $\mu$ on the \\" + str(
        round(data_1D.time[-1] - data_1D.time[plt_min], 2)) + " last seconds \end{flushleft}"
    ax1.plot(theta, theorique * 1000, label="Theorical")
    ax1.plot(theta, mean * 1000, label=lab)
    ax1.fill_between(theta, y1=(mean + std) * 1000, y2=(mean - std) * 1000, alpha=0.5, color="r",
    label=r"$\mu$ +/- $\sigma$")
    ax1.annotate(r"$\bar{\sigma}$ = " + str(round(np.mean(std * 1000), 2)), (67.5, 2), bbox=bbox)
    ax1.vlines(theta_max, 0, 14, colors="k", linestyles="--", label=r"$\Theta_{max}$ =" + str(theta_max) + " deg")
    ax1.legend(loc="upper left")
    ax1.set_xlabel("$\Theta$ (deg)")
    ax1.set_ylabel("$e_{film}$ (mm) ")
    ax1.set_xticks([0, 45, 90, 135, 180])
    ax1.set_xlim([0.0, 180])
    ax1.grid(visible=True)

    plt.subplot(1, 2, 2)

    ax2.plot(data_1D.time, convergence)
    ax2.vlines(data_1D.time[plt_min], 0, 1, colors="k", linestyles="--",
               label=f"Start average time {data_1D.time[plt_min]} s")

    plt.title("Convergence")
    ax2.set_xlabel("Physical time (s)")
    ax2.set_ylabel(" $\int_{\Gamma}   |e_{film}(t) - e_{film}(t+dt))| /  \int_{\Gamma}   |e_{film}(t)| $")
    ax2.set_xlim((data_1D.time[0], data_1D.time[-1]))
    ax2.set_ylim(0, 1)
    ax2.legend(loc="upper right")
    ax2.grid(visible=True)
    savefig("e_film", format="png", pickle=fig, dpi=1000)
    plt.show()

    # ***************************** Film thickness -  90 to theta max
    #theta_max = 90

    oscillation_0, oscillation_45, oscillation_90, oscillation_135, oscillation_max = [], [], [], [], []
    for i in range(plt_min, len(data_1D.key_list)):
        df = data_1D[data_1D.key_list[i]].loc[data_1D[data_1D.key_list[i]]["theta_interface"] < theta_max]
        f1 = interp1d(df["theta_interface"], df["Film thickness"],
                      kind='cubic', fill_value="extrapolate")

        oscillation_0.append(f1(0) * 1000)
        oscillation_45.append(f1(45) * 1000)
        oscillation_90.append(f1(90) * 1000)
        oscillation_135.append(f1(135) * 1000)
        oscillation_max.append(f1(theta_max) * 1000)

    x = data_1D.time[plt_min:201]

    # FFT of oscillations

    from modules.signal_treatment.FFT import FFT

    def FFT_plot(oscillation, filename, theta, sr=500):
        """
        Perform FFT on film thickness
        :param oscillation: Liste with the film thickness at given theta
        :param filename: output graph filename
        :param sr: sample rate 1/s
        :return:
        """
        freq, mag = FFT(x, oscillation, sr=sr, norm=True)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        set_size(subplots=(1, 2))

        def maximums(X, Y, max_number=1):
            if max_number > len(Y):
                raise Exception("max_number cannot higher than the length of the input list.")
            import copy
            L = copy.deepcopy(list(Y))
            XX = copy.deepcopy(list(X))
            YY = copy.deepcopy(list(Y))
            y_maximum = []
            x_maximum = []
            while len(y_maximum) < max_number:
                m = max(L)
                y_maximum.append(m)
                idx = YY.index(m)
                x_maximum.append(XX[idx])
                L.remove(m)
            return x_maximum, y_maximum

        x_maxi, y_maxi = maximums(freq[0:len(freq) // 2], mag[0:len(freq) // 2], max_number=2)
        print("Maximum frequency")
        print(x_maxi)
        s = ''
        for i, (elem) in enumerate(x_maxi):
            if i != len(x_maxi):
                s += r'$f_{' + str(i) + r'}$ = ' + str(round(elem, 2)) + ' Hz' + "\n"
            else:
                s += r'$f_{' + str(i) + r'}$ = ' + str(round(elem, 2)) + ' Hz'
        ax1.annotate(s, (50, 0.5), bbox=bbox)
        ax1.scatter(x_maxi, y_maxi, marker="x")
        ax1.fill_between(freq, y1=[0] * len(mag), y2=mag, alpha=.5, color="r")
        ax1.set_xlabel("Freq. (Hz)")
        ax1.set_ylabel(r'FFT Amplitude $|X(freq)|/\rm{max}(|X(freq)|$)')
        ax1.set_xlim(0, len(freq) // 2)
        ax1.set_ylim(0, 1)
        ax1.grid(visible=True)

        ax2.plot(x, oscillation, label=r"$\Theta$ = " + str(round(theta, 0)))
        ax2.set_ylabel("$e_{film}$ (mm) ")
        ax2.set_xlabel("Physical time (s)")
        ax2.set_xlim([x[0], x[-1]])
        ax2.grid(visible=True)
        savefig(filename, format="png", pickle=fig, dpi=1000)
        plt.show()

    # Oscillation graph
    FFT_plot(oscillation_0, f"e_film_FFT_0", theta=0)
    FFT_plot(oscillation_45, f"e_film_FFT_45", theta=45)
    FFT_plot(oscillation_90, f"e_film_FFT_90", theta=90)
    FFT_plot(oscillation_135, f"e_film_FFT_135", theta=135)
    FFT_plot(oscillation_max, f"e_film_FFT_{theta_max}", theta=theta_max)

if __name__ == "__main__":

    paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
    print("--- load DIVA input")
    DIVA_input = DIVA_in.diva_input()
    DIVA_input.load(paf + "/run")
    time = pd.read_csv(paf + "post_traitement/time.csv", sep=";")
    time = np.array(time["time (s)"])
    df_interface = pr()
    df_interface.load_folder(paf + "post_traitement/data1D/interface")
    df_interface.define_time(time)  # Associated a time list with the data
    theta_max = 170
    t_min = 0.3
    film_tchikness(df_interface,DIVA_input , t_min, theta_max)

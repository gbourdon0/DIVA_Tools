from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
import modules.post_proc_2D as pt
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
import seaborn as sns
from scipy.optimize import minimize
import pandas as pd
paf = "/work/gbourdon/02_benchmark_FC72/13_0/"
configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/images")
bbox = dict(boxstyle="round", fc="1")
import time

# load data
# time = pd.read_csv(paf + "/time.csv", sep=";")
# time = np.array(time["time (s)"])
data_1D = pr()
data_1D.load_file(paf + "/post_traitement/data2D/200.pickle")
# data_1D.define_time(time)  # Associated a time list with the data
#
import copy

df = data_1D["200.pickle"]
print(df.columns)
df2 = copy.deepcopy(df)
df2["abs_phi_sol"] = abs((df["Phi_solid"]))
step = abs(df["R"][0] - df["R"][1])
print(step)
dr = 5e-5 # Integration step in meter
df2 = df.loc[abs(df["Phi_solid"]) < 2 * step]
df3 = df.loc[abs(df["Phi"]) < 2 * step]
theta = np.arange(2, 90, 1)

print("Finding lines")


def find_line(theta, guess=[0.0, 0.0]):
    out = []

    def f_solid(r, theta):
        u_theta = r * np.array([np.sin(np.deg2rad(theta)), -np.cos(np.deg2rad(theta))])
        out = abs(
            pt.interp2D(np.array(df2["Phi_solid"]), np.array(df2["R"]), np.array(df2["Z"]), u_theta[0], u_theta[1],
                        resolve_nan=True))  # to find the minimum value which is zero
        return out

    def f_liq(r, theta):
        u_theta = r * np.array([np.sin(np.deg2rad(theta)), -np.cos(np.deg2rad(theta))])
        out = abs(pt.interp2D(np.array(df3["Phi"]), np.array(df3["R"]), np.array(df3["Z"]), u_theta[0], u_theta[1],
                              resolve_nan=True))  # to find the minimum value which is zero
        return out

    for t in theta:
        print(t)
        start = minimize(f_solid, np.array(guess[0]), args=(t,), method='Nelder-Mead', tol=1e-8).x
        end = minimize(f_liq, np.array(guess[1]), args=(t,), method='Nelder-Mead', tol=1e-8).x
        out.append((start, end))
        guess = [start, end]
    return out


lines = find_line(theta, guess=[5e-3, 5e-3])


def plot():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    for elem, t in zip(lines, theta):
        print(t)
        start = elem[0] * np.array([np.sin(np.deg2rad(t)), -np.cos(np.deg2rad(t))])
        end = elem[1] * np.array([np.sin(np.deg2rad(t)), -np.cos(np.deg2rad(t))])
        plt.scatter(start[0], start[1])
        plt.scatter(end[0], end[1])
    extent = [df["R"].min(), df["R"].max(), df["Z"].min(), df["Z"].max()]
    toplot = np.array(df["Temperature"]).reshape(1024, 512)
    img = ax.imshow(toplot, extent=extent, origin="lower")
    cb = fig.colorbar(img)
    cb.set_label("temperature")
    iso_lines = ["Phi", "Phi_solid"]
    from modules.global_variable.param import plot_param

    for line in iso_lines:
        line_to_plot = np.array(df[line]).reshape(1024, 512)
        ct = ax.contour(line_to_plot, levels=[0], linewidths=plot_param["linewidths"],
                        linestyles=plot_param["linestyles"], zorder=plot_param["zorder"], extent=extent)
    plt.show()


# ***************************** Mean(gradP) as function of theta
mean_cub, mean_lin, mean_near = [], [], []
std_cub, std_lin, std_near = [], [], []
for r, angle in zip(lines, theta):
    print(angle)

    # To select the area to interpolate. This to avoid jump of pressure to influence the interpolation and speed it up.
    # Define and area around the given theta (to speed up the interpolation)
    dtheta = 5
    x_up1, y_up1 = float(r[1] * np.sin(np.deg2rad(angle + dtheta))), float(-r[1] * np.cos(np.deg2rad(angle + dtheta)))
    x_down1, y_down1 = float(r[1] * np.sin(np.deg2rad(angle - dtheta))), float(
        -r[1] * np.cos(np.deg2rad(angle - dtheta)))
    x_up2, y_up2 = float(r[0] * np.sin(np.deg2rad(angle + dtheta))), float(-r[0] * np.cos(np.deg2rad(angle + dtheta)))
    x_down2, y_down2 = float(r[0] * np.sin(np.deg2rad(angle - dtheta))), float(
        -r[0] * np.cos(np.deg2rad(angle - dtheta)))
    # Define the quare according the area around theta
    y_min, y_max = min(y_up1, y_down1, y_down2, y_up2), max(y_up1, y_down1, y_down2, y_up2)
    x_min, x_max = min(x_up1, x_down1, x_down2, x_up2), max(x_up1, x_down1, x_down2, x_up2)
    # In the selection, we exclude point in the solid and liquid (to avoid jump of pressure)
    df4 = df.loc[(df["R"] <= x_max) & (df["R"] >= x_min) & (df["Z"] >= y_min) & (df["Z"] <= y_max) &
                 (df["Phi_solid"] < 0.0 - step) & (df["Phi"] < 0.0 - step)]


    # Define interpolation functions
    def f_nearest(r, theta):
        u_theta = r * np.array([np.sin(np.deg2rad(theta)), -np.cos(np.deg2rad(theta))])
        out = pt.interp2D(np.array(df4["\/Pressure_r"]), np.array(df4["R"]), np.array(df4["Z"]), u_theta[0], u_theta[1],
                          resolve_nan=True, kind='nearest')
        return out


    def f_linear(r, theta):
        u_theta = r * np.array([np.sin(np.deg2rad(theta)), -np.cos(np.deg2rad(theta))])
        out = pt.interp2D(np.array(df4["\/Pressure_r"]), np.array(df4["R"]), np.array(df4["Z"]), u_theta[0], u_theta[1],
                          resolve_nan=True, kind='linear')
        return out


    def f_cubic(r, theta):
        u_theta = r * np.array([np.sin(np.deg2rad(theta)), -np.cos(np.deg2rad(theta))])
        out = pt.interp2D(np.array(df4["\/Pressure_r"]), np.array(df4["R"]), np.array(df4["Z"]), u_theta[0], u_theta[1],
                          resolve_nan=True, kind='cubic')
        return out


    # Compute value along the radius with a step
    how = int(abs(r[0] - r[1])/(step))+1
    print(how)
    how = 10
    r_int = np.arange(r[0], r[1], abs(r[0] - r[1])/how)
    nan_check = np.array([np.nan], dtype='float64')[0]
    cubic = np.array([f_cubic(rr, angle) for rr in r_int if not np.isnan(f_cubic(rr, angle))])
    r_cub = np.array([rr for rr in r_int if not np.isnan(f_cubic(rr, angle))])
    linear = np.array([f_linear(rr, angle) for rr in r_int if not np.isnan(f_linear(rr, angle))])
    r_linear = np.array([rr for rr in r_int if not np.isnan(f_linear(rr, angle))])
    nearest = np.array([f_nearest(rr, angle) for rr in r_int if not np.isnan(f_nearest(rr, angle))])
    r_near = np.array([rr for rr in r_int if not np.isnan(f_nearest(rr, angle))])

    # Show them to check
    '''plt.scatter(r_near, nearest, label="Nearest")
    plt.scatter(r_cub, cubic, label='Cubic')
    plt.scatter(r_linear, linear, label='Linear')
    plt.legend()
    plt.show()'''

    # Compute mean integral
    mean_near.append(float(np.trapz(cubic, r_cub) / abs(r[0] - r[1])))
    mean_cub.append(float(np.trapz(nearest, r_near) / abs(r[0] - r[1])))
    mean_lin.append(float(np.trapz(linear, r_linear) / abs(r[0] - r[1])))

    std_cub.append(np.trapz((cubic - mean_cub[-1]) ** 2, r_cub))
    std_lin.append(np.trapz((linear - mean_lin[-1]) ** 2, r_linear))
    std_near.append(np.trapz((nearest - mean_near[-1]) ** 2, r_near))

mean_near, mean_cub, mean_lin = np.array(mean_near), np.array(mean_cub), np.array(mean_lin)
std_cub, std_lin, std_near = np.array(std_cub), np.array(std_lin), np.array(std_near)
plt.plot(theta, mean_cub, label='Cubic', color='r')
plt.fill_between(theta, y1=(mean_cub + std_cub), y2=(mean_cub - std_cub), alpha=0.5, color="r",
                 label=r"$\mu$ +/- $\sigma$ - Cubic")
plt.plot(theta, mean_near, label="Nearest", color="b")
plt.fill_between(theta, y1=(mean_near + std_near), y2=(mean_near - std_near), alpha=0.5, color="b",
                 label=r"$\mu$ +/- $\sigma$ - Near")
plt.plot(theta, mean_lin, label="Linear", color="g")
plt.fill_between(theta, y1=(mean_lin + std_lin), y2=(mean_lin - std_lin), alpha=0.5, color="g",
                 label=r"$\mu$ +/- $\sigma$ - Linear")
plt.legend()
savefig("gradP_r", format="png", dpi=1000)
plt.show()

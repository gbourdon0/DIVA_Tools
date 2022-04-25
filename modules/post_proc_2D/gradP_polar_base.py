from modules.data_reader.pickle_reader import PickleReader as pr
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from modules.data_reader.Tecplot import Tecplot
import modules.post_proc_2D as pt
from scipy.interpolate import interp1d
from modules.plot.matplotlib_setup import configure_latex, set_size, savefig
import numpy as np
########################################################################################################################
#                                                       INPUT
########################################################################################################################
THETA = np.arange(3, 177, 1) # Range of angle (0,180)
FRAME = 1 #frame to analyze
DEBUG = False #if debug needed, will plot graph
DR = 1e-6 # radial step for computation of the mean
PAF = "/work/gbourdon/02_benchmark_FC72/13_0/"
configure_latex(style="seaborn-bright", global_save_path=PAF + "post_traitement/images")

tec = Tecplot()
tec = tec.open_pickle(PAF + "/post_traitement/data2D/170.pickle")
print(tec.get_header())
DX = tec.dx[0] #DX (or DY assume grid is uniform)


# ************************************* INTERPOLATE PHI = 0 as a function of theta
#   get film and solid
THETA = THETA-90 #more convecnient for computation
phi_x, phi_y = tec.get_film_interface(frame=FRAME, phi_liq_name="Phi", phi_sol_name="Phi_solid")
phi_sol_x, phi_sol_y = tec.get_iso_value_2D(frame=1, var_name="Phi_solid", iso_values=[0])


def to_polar(x, y):
    import copy
    is_x_negative = copy.deepcopy(x)  # Pour avoir de 0 a 360 deg
    is_x_negative[x < 0] = 1
    is_x_negative[x >= 0] = 0
    R = np.sqrt(x ** 2 + y ** 2)
    Theta = np.arctan(y / x) + is_x_negative * np.pi

    return R, np.rad2deg(Theta)


# transform to polar coordinate
phi_r, phi_theta = to_polar(phi_x, phi_y)
phi_sol_r, phi_sol_theta = to_polar(phi_sol_x, phi_sol_y)
# interp functions
phi_fun = interp1d(phi_theta, phi_r, bounds_error=False, fill_value="extrapolate", kind="linear")
phi_sol_fun = interp1d(phi_sol_theta, phi_sol_r, bounds_error=False, fill_value="extrapolate", kind="linear")

# get the interpolated values of radius
r_solid = phi_sol_fun(THETA)
r_phi = phi_fun(THETA)

if DEBUG:
    def to_cartesien(r, theta):
        theta = theta
        x = r / np.sqrt((1 + np.tan(np.deg2rad(theta)) ** 2))
        y = x * np.tan(np.deg2rad(theta))
        return x, y


    x_sol, y_sol = to_cartesien(r_solid, THETA)
    x_phi, y_phi = to_cartesien(r_phi, THETA)

    tec.plot(flood="Theta_polar", lines=["Phi", "Phi_solid"], scatter=[x_phi, y_phi])

# ************************************* get the pressure along the axis

data_reduce = tec[FRAME].data
step = abs(data_reduce["R"][0] - data_reduce["R"][1])
print(step)
mean_gradP,std_gradP = [],[]
mean_P,std_P = [],[]
for i in range(len(r_solid)):
    start = r_solid[i]+2*DX
    end = r_phi[i]-2*DX
    data_reduce = tec[FRAME].data
    data_reduce = data_reduce.loc[(data_reduce["R_polar"]<1.1*end) &(data_reduce["Phi_solid"]<-DX) &(data_reduce["Phi"]<-DX)]
    # value along a radius
    r = np.arange(start+DX, end-DX, DR)

    theta = np.array([THETA[i]+90]* len(r))


    P = pt.interp2D(data_reduce["Pressure"],data_reduce["R_polar"], data_reduce["Theta_polar"],r,theta,
                        kind = "linear")


    gradP = np.gradient(P,DR)



    mean_gradP.append(np.mean(gradP))
    std_gradP.append(np.std(gradP))
    mean_P.append(np.mean(P))
    std_P.append(np.std(P))

mean_gradP = np.array(mean_gradP)
std_gradP = np.array(std_gradP)

mean_P = np.array(mean_P)
std_P = np.array(std_P)

plt.plot(THETA+90,mean_gradP)
plt.fill_between(THETA+90, y1=(mean_gradP + std_gradP), y2=(mean_gradP - std_gradP), alpha=0.5, color="r",
                 label=r"$\mu$ +/- $\sigma$ - Linear")
plt.xlabel(r"$\theta$ (deg)")
plt.ylabel(r"$\nabla P_r$ (Pa/m)")
plt.show()

plt.plot(THETA+90,mean_P)
plt.fill_between(THETA+90, y1=(mean_P + std_P), y2=(mean_P - std_P), alpha=0.5, color="r",
                 label=r"$\mu$ +/- $\sigma$ - Linear")
plt.xlabel(r"$\theta$ (deg)")
plt.ylabel(r"$P$ (Pa)")
plt.show()
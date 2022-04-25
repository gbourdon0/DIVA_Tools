from script.post_traitement_2Daxi.old.graph_1D_epaisseur import film_tchikness
from script.post_traitement_2Daxi.old.graph_1D_solid import wall_heat_flux
from script.post_traitement_2Daxi.old.graph_1D_interface import interface_heat_flux
from modules.plot.matplotlib_setup import configure_latex
import pandas as pd
import numpy as np
from modules.data_reader.pickle_reader import PickleReader as pr
import modules.diva_input as DIVA_in

# Load files
paf = "/work/gbourdon/02_benchmark_FC72/06_1d-1/"

configure_latex(style="seaborn-bright", global_save_path=paf + "post_traitement/images")

# load data
print("LOADING DATA")
print("--- load interface data")
time = pd.read_csv(paf + "post_traitement/time.csv", sep=";")
time = np.array(time["time (s)"])
df_interface = pr()
df_interface.load_folder(paf + "post_traitement/data1D/interface")
df_interface.define_time(time)  # Associated a time list with the data
print(df_interface.get_header())
print("--- load wall data")
df_wall = pr()
df_wall.load_folder(paf + "post_traitement/data1D/wall")
df_wall.define_time(time)
print("--- load DIVA input")
DIVA_input = DIVA_in.diva_input()
DIVA_input.load(paf + "/run")

#FILM THICKNESS
theta_max = 170
t_min = 0.1
film_tchikness(df_interface,DIVA_input , t_min, theta_max)

#WALL HEAT FLUX
t_min = 0.3
wall_heat_flux(df_wall,t_min)

# INTERFACE HEAT FLUX
theta_max = 170
t_min = 0.3
interface_heat_flux(df_interface, t_min, theta_max)

# Wall heat flux = f(epaissuer)

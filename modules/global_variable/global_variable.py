import pandas as pd
import modules.diva_input as DIVA_in
from modules.data_reader.Tecplot import Tecplot

# Input from DIVA initialisation
DIVA_input = DIVA_in.diva_input()
DIVA_plt = Tecplot()
DIVA_0D = pd.DataFrame()

# Output Dataset initialisation
data_1D = pd.DataFrame()
data_0D = pd.DataFrame()

# Numerical definition
zero = float(0)

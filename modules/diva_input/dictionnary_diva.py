"""
Create all dictionnary to translate DIVA input into spoken language.
"""
# Temporal and spatial configuration
coord_sys = {1: "2D cartesian", 2: "Axisymetrical", 3: "3D cartesian"}
mesh_type = {0: "Uniform grid", 1: "Non uniform grid", 2: "Mixed grid"}
mesh_non_u = {1: "Coarsening Argsh", 2: "Coarsening Sh", 3: "Refinement Argsh", 4: "Refinement Sh"}
mesh_mirror = {0: "No mirror", 1: "Mirror mesh"}
drop_or_bubbles = {0: "One phase flow", 1: 'Drops', 2: 'Bubbles'}
immersed_boundary = {0: "No immersed boundary", 1: "Solid immersed Boundary", 2: "I don't know"}
marangoni = {0: "Thermal", 1: "Solutal", 2: "Muragolu law"}
variable_viscosity = {0: "Constant mu", 1: "Variable viscosity Sutherland law"}
enthal_diff = {0: "No enthalpy diffusion", 1: "Enthalpy diffusion"}

# Boundary Condition
BC_vitesse = {1: "Moving or static wall", 2: "Symmetric", 3: "Free", 4: "Periodic", 5: "Injection"}
BC_vitesse_turb = {0: "No turbulent inflow", 1: "Turbulent inflow"}

# Initial Condition
benchmark = {0: "No benchmark", 1: "benchmark"}
backup = {0: "Not started from backup", 1: "started from backup"}
v_init = {0: "No initial speed", 1: "initial speed"}
T_init = {0: "No initial temperature", 1: "initial temperature"}
mass_frac_init = {0: "No initial mass fraction", 1: "initial mass fraction"}

# Mass Fraction boundary condition
BC_mass_frad = {1: "Uniform Dirichlet", 2: "Non uniform Dirichlet", 3: "Uniform Neumann", 4: "Non uniform Neumann",
                5: "Non uniform Robin", 6: "Periodic"}

# Temperature boundary condition
BC_temperature = {1: "Uniform Dirichlet", 2: "Non uniform Dirichlet", 3: "Uniform Neumann", 4: "Non uniform Neumann",
                  5: "Non uniform Robin", 6: "Periodic", 7: "Wall Dirichlet"}
# Numerical solver
rk = {1: "First order", 2: "2nd order", 3: "3rd order"}
interface_solv = {0: "One phase flow", 1: "Level Set Method"}
navier_stokes = {0: "No Navier-Stokes", 1: "Incompressible", 2: "Variable density", 3: "Semi-implicit compressible"}
pressure = {1: "BBMG", 2: "BBMG-PCG", 3: "JPCG"}
viscous = {0: "Inviscid flow", 1: "Semi conservative viscous method", 2: "Conservative viscous method"}
time_discrt = {1: "Explicit", 2: "Implicit"}
viscous_dissip = {0: "Viscous dissipation disable", 1: "Viscous dissipation enable"}

temperature = {0: "No temperature", 1: "Temperature"}
phase_change = {0: "No phase change", 1: "Boiling", 2: "Evaporating", 3: "Boiling and evaporation"}
mass_frac = {0: "No mass fraction", 1: "Mass fraction"}
GFM_div_corr = {0: "No divergence correction on GFM", 1: "Divergence correction on GFM"}
GFM_temp_ext = {0: "No Aslam extension", 1: "Aslam constant extension", 2: "Aslam linear extension",
                3: "Aslam quadratic extension"}
write_all_data = {0: "Don't write all data file", 1: "write all data file"}

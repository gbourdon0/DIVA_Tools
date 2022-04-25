# Create a table with vapuid and fluid properties
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from modules.data_reader.plt_obj import plt_obj as plt_object
from modules.global_variable.default_param import default_plot_param
import modules.global_variable.global_variable as gv
from scipy import constants
import matplotlib
from matplotlib.offsetbox import AnchoredText
import matplotlib.patches as mpatches
import modules.diva_input as DIVA
import pandas as pd
import numpy as np

def liquid_gas_properties(paf,v_init = np.nan, D_cara = np.nan, format = "csv"):

    #Start with the gas
    import plotly.graph_objects as go
    '''prop = [r"$\rho$", r"$\rho$", r"$\rho$", r"$\rho$"]
    fig = go.Figure(data=[go.Table(header=dict(values=['Properties', 'vapuid', 'Gas']),
                                   cells=dict(values=[prop,[100, 90, 80, 90], [95, 85, 75, 95]]))
                          ])

    fig.show()
    fig.write_image(paf + "vapuidGasProperties.png")'''

    prop = [r"$\kappa$, thermal conductivity [W/m/K]",r"$\rho$, density [kg/m$^3$]",
           r"$C_p$ heat capacity  [J/kg/K]" ,r"$\mu$, dynamic viscosity [Pa.s]", r"$L_v$, latent heat  [J/kg]",
            r"$\gamma$, superficial tension [N/m]",r"$T_{sat}$, saturation temperature [K]",
        r"$\Delta~T_{sub}$, subcooling [K]", "Injection velocity [m/s]","Reynolds","Prandtl","Ja","Ra","Gr"
        ]

    df = pd.DataFrame()
    df["Properties"]= prop
    print("WARNING : Dilatation coefficient is taken as 1/Tp_inf !!!")
    beta = 1/gv.DIVA_input.IC.Tp_inf
    nu_gas = gv.DIVA_input.PP.mu_vap/gv.DIVA_input.PP.rho_vap
    alpha_gas = gv.DIVA_input.TP.kth_vap/(gv.DIVA_input.PP.rho_vap * gv.DIVA_input.TP.cp_vap)
    print(nu_gas)
    print(alpha_gas)
    exp_digit = 1
    precision = 2
    df["Liquid"] = [
        np.format_float_scientific(gv.DIVA_input.TP.kth_liq, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.rho_liq, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.cp_liq, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.mu_liq, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.hfg, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.sigma, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.t_sat, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.IC.DT_sub, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(v_init, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.rho_liq*D_cara*v_init/gv.DIVA_input.PP.mu_liq, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.mu_liq * gv.DIVA_input.TP.cp_liq/gv.DIVA_input.TP.kth_liq, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.cp_liq*gv.DIVA_input.IC.DT_sub/gv.DIVA_input.TP.hfg, unique=False, exp_digits=exp_digit, precision=precision),
        np.nan,
        np.nan
    ]

    df["Gas"] = [
        np.format_float_scientific(gv.DIVA_input.TP.kth_vap, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.rho_vap, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.cp_vap, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.mu_vap, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.hfg, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.sigma, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.t_sat, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.IC.DT_sub, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(v_init, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.rho_vap*D_cara*v_init/gv.DIVA_input.PP.mu_vap, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.PP.mu_vap * gv.DIVA_input.TP.cp_vap/gv.DIVA_input.TP.kth_vap, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(gv.DIVA_input.TP.cp_vap*(gv.DIVA_input.IC.T_immersed-gv.DIVA_input.TP.t_sat)/gv.DIVA_input.TP.hfg, unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(
            constants.g * D_cara ** 3 * (gv.DIVA_input.IC.T_immersed - gv.DIVA_input.IC.Tp_inf) * beta / (
                        nu_gas * alpha_gas), unique=False, exp_digits=exp_digit, precision=precision),
        np.format_float_scientific(constants.g * D ** 3 * (gv.DIVA_input.IC.T_immersed - gv.DIVA_input.IC.Tp_inf) * beta * gv.DIVA_input.PP.rho_vap ** 2 / (
                    gv.DIVA_input.PP.mu_vap ** 2), unique=False, exp_digits=exp_digit, precision=precision)
    ]

    df.set_index("Properties", inplace = True)

    #Writing
    if format == "csv":
        df.to_csv(paf +"FluidLiquidProperties.csv", sep = ";")
    elif format == "excel":
        pd.to_excel(paf +"FluidLiquidProperties.csv")
    elif format =="png":
        col = ["Properties"] + list(df.columns)
        fig = go.Figure(data=[go.Table(header=dict(values=col),
                                       cells=dict(values=[prop,df["Liquid"], df["Gas"]]))
                              ])

        fig.show()
        fig.write_image(paf + "FluidLiquidProperties.png")
    elif format == "latex":
        df.to_latex(paf + "FluidLiquidProperties.tex")
    return df


if __name__ == "__main__":
    paf = "/home/gbourdon/03_DIVA_dev/000_BENCHMARK/05_conv_nat_benchmark/run"
    gv.DIVA_input = DIVA.diva_input()
    gv.DIVA_input.load(paf)
    D =3.56e-2
    print(f"radius = {D/2}")
    print(f"box = {D/2/0.2}")
    out = liquid_gas_properties(paf = "/home/gbourdon/03_DIVA_dev/000_BENCHMARK/05_conv_nat_benchmark/",v_init=0,D_cara =D, format = "csv")

    old_Ra = float(out["Gas"]["Ra"])
    new_D = (D**3*1e6/old_Ra)**(1/3)
    print(new_D)
    print(out)



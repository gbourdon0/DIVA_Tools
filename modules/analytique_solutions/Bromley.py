import matplotlib.pyplot as plt
import scipy.constants as sc
import numpy as np


def h(liquid, gas, Tw, U, D, radiation=False, **kwargs):
    """
    This formula is taken from Bromley (1950) and Bromley et al (1953).
    - Horizontal cylinder
    - Saturation liquid
    - natural convection and forced convection (according Fr number)
    - radiation integration if necessary
    :return:
    """
    cst1 = 0.62 #experimental constant
    cst2 = 2.7 #experimental constant
    Fr = U / np.sqrt(sc.g * D)
    DT_sup = Tw - liquid.tsat
    llambda = liquid.hfg * (1 + 0.4 * DT_sup * gas.cp / liquid.hfg) ** 2

    if radiation:
        try:
            hr = (sc.Stefan_Boltzmann / (1 / kwargs["eps_sol"] + 1 / kwargs["eps_liq"] - 1)) * (
                        Tw ** 4 - liquid.T ** 4) / (DT_sup)
        except:
            raise Exception("Something went wrong while computing radiatif terms. Please check if you put eps_sol and "
                            "eps_liq (emissivity of liquid and solid) in kwargs")

    if Fr < 1.0:
        hco = cst1 * (gas.k ** 2 * (liquid.rho - gas.rho) * gas.rho * sc.g * llambda * gas.cp / (
                    DT_sup * D * gas.Pr)) ** .25

        if radiation:
            from scipy.optimize import fsolve
            h = hco + 3 / 4 * hr
        else:
            h = hco
    elif Fr > 2.0:
        hco = cst2 * np.sqrt(U * gas.k * gas.rho * llambda / (D * DT_sup))
        if radiation:
            h = hco + 7 / 8 * hr
        else:
            h = hco
    else:
        raise NotImplementedError(f"The correlation is not defined for Fr in [1.0;2.0]. Fr = U/sqrt(gD) = {Fr} ")

    return h

if __name__ == "__main__":
    import modules.diva_input as DIVA

    DIVA_input = DIVA.diva_input()
    DIVA_input.load("/home/gbourdon/04_DIVA_benchmark_thermal/02_Bromley/01_test/run")

    U = DIVA_input.BC.BC_Y1[1]
    D = DIVA_input.IC.solid_obj_dim[1]
    DT = DIVA_input.IC.T_immersed - DIVA_input.TP.t_sat
    print(DT)
    h_test = h(DIVA_input.liq, DIVA_input.gas, DIVA_input.IC.T_immersed, U, D, radiation=False)
    print(h_test)
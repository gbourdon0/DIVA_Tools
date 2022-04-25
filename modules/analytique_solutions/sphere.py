import scipy.constants as cst
import numpy as np
import modules.diva_input as DIVA_in


def film_tchikness(diva_input, D, theta, dtheta=1.0):
    """
    Compute the film thickness according the angle (define at 0 at the bottom of the sphere). This is the formula from
    Schilchting H. (1968), Boundary Layer Theory Theory, chapter XI.
    This suppose :
    - Neglecting sensible heat
    - mu_v/mu_l -> 0
    - Inertia and convection term neglected -> u_l = 0 everywhere in the liquid
    - Isothermal wall temperature
    :param dtheta: dtheta step for the integration in the formula
    :param theta: The angle where the thickness will be compute
    :param diva_input: a diva_input object (to get fluid and vapor properties
    :param D: diameter of the sphere
    :return: thickness according theta
    """

    alpha_v = diva_input.TP.kth_vap / (diva_input.PP.rho_vap * diva_input.TP.cp_vap)
    nu_v = diva_input.PP.mu_vap / diva_input.PP.rho_vap
    Ja = diva_input.TP.cp_vap * (diva_input.IC.T_immersed - diva_input.TP.t_sat) / diva_input.TP.hfg
    Ra = cst.g * D ** 3 * (diva_input.PP.rho_liq - diva_input.PP.rho_vap) / (nu_v * alpha_v * diva_input.PP.rho_vap)
    R = D / 2

    integration_range = np.arange(0, np.deg2rad(theta+dtheta), np.deg2rad(dtheta))
    integrande = np.sin(integration_range) ** (5 / 3)
    integral = np.trapz(integrande, integration_range)
    thick = 2 * ((8 * Ja / Ra) ** .25) * R * integral / (np.sin(np.deg2rad(theta)) ** (8 / 3))

    return thick


def Nu_cf_dhir(diva_input, D, U):
    """
    Compute the Nusselt for forced convection as in Dhir et Purohit (1978), Subcooled film-boiling heat transfer
    from spheres
    :return: Nusselt
    """

    rho_v = diva_input.PP.rho_vap
    rho_l = diva_input.PP.rho_liq
    hfg = diva_input.TP.hfg
    mu_v = diva_input.PP.mu_vap
    mu_l = diva_input.PP.mu_liq
    k_v = diva_input.TP.kth_vap
    k_l = diva_input.TP.kth_liq
    cp_v = diva_input.TP.cp_vap
    cp_l = diva_input.TP.cp_l
    mu = mu_v / mu_l

    Tliq = diva_input.IC.Tp_int
    Tw = diva_input.IC.T_immersed
    Tsat = diva_input.TP.t_sat
    DT_sup = Tw-Tsat
    DT_sub = Tsat-Tliq

    Ja_sub = cp_l*DT_sub/hfg
    Ja_sup = cp_v*DT_sup/hfg
    Pr_v = mu_v*cp_v/k_v
    Pr_l = mu_l*cp_l/k_l
    Re = rho_l*U*D/mu_l


    Nu0 = 0.8*(cst.g*rho_v*(rho_l-rho_v)*hfg*D**3 / (mu_v*k_v*DT_sup))
    Nu = Nu0 + 0.8*Re**.5 * ( 1 + Ja_sub*Pr_v/(Ja_sup*Pr_l*mu))
    return Nu

if __name__ == "__main__":
    theta = np.arange(1,90,1)
    theorique =[film_tchikness(DIVA_input,D = 10e-3,theta = angle,dtheta = 0.1) for angle in theta]
    import matplotlib.pyplot as plt
    plt.plot(theta, theorique)
    plt.show()
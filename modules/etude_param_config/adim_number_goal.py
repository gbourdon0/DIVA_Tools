from iapws import IAPWS97
from modules.etude_param_config.adim_number import *
###################
#User input
##################

P0 = 0.1 #Mpa
Tliq = 20+273.15
Timmersed = 875+273.15
Tsat = IAPWS97(P=P0,x=0).T
water = IAPWS97(P=P0, T=Tliq)
steam = IAPWS97(P=P0, x= 1)
hfg = (IAPWS97(T = Tsat, x=1).h - IAPWS97(T=Tsat,x=0).h)*1000

goal_param = {
    "Tliq": Tliq,
    "Timmersed": Timmersed,
    "Tsat":Tsat,
    "rho_liq": water.rho,
    "rho_vap": steam.rho,
    "cp_liq": water.cp*1000,
    "cp_vap": steam.cp*1000,
    "mu_liq": water.mu,
    "mu_vap":steam.mu,
    "k_liq" :water.k,
    "k_vap": steam.k,
    "hfg": hfg ,
    "D": 10e-3,
    "u" : 0.0
}




def refresh_adim(dictionnary):
    out = {
        "Ja_sup": Ja_sup(dictionnary["cp_vap"], dictionnary["hfg"], dictionnary["Timmersed"], dictionnary["Tsat"]),
        "Ja_sub": Ja_sub(dictionnary["cp_liq"], dictionnary["hfg"], dictionnary["Tsat"], dictionnary["Tliq"]),
        "Re_liq": Re(dictionnary["mu_liq"], dictionnary["D"], dictionnary["u"], dictionnary["rho_liq"]),
        "Pr_vap": Pr(dictionnary["mu_vap"], dictionnary["cp_vap"], dictionnary["k_vap"]),
        "Pr_liq": Pr(dictionnary["mu_liq"], dictionnary["cp_liq"], dictionnary["k_liq"]),
        "rapport_rho": dictionnary["rho_liq"] / dictionnary["rho_vap"],
        "rapport_mu": dictionnary["mu_liq"] / dictionnary["rho_vap"]
    }
    return out

goal_adim = refresh_adim(goal_param)
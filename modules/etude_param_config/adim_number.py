from scipy.constants import constants


def Pr(mu, cp, k):
    return mu * cp / k


def Ja_sup(cp, hfg, Timmersed, Tsat):
    DT = Timmersed - Tsat
    return cp * DT / hfg


def Ja_sub(cp, hfg, Tsat, Tliq):
    DT = Tsat - Tliq
    return cp * DT / hfg


def Re(mu, D, u, rho):
    return rho * D * u / mu


def Gr(Thot, Tcold, D, rho, mu):
    """
    Compute Grasshoff number.Assume Tcold if for a liquid or gas
    :param Thot: hottest temperature
    :param Tcold: coldest temperature
    :param D: caracteristic dimension
    :param rho: density
    :param mu: viscosity
    :return:
    """
    DT = Thot - Tcold
    beta = 1 / Tcold
    constants.g * beta * DT * D ** 3 * rho ** 2 / mu ** 2

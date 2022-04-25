import math
import numpy as np
from scipy import constants
from scipy.optimize import minimize
import sys
sys.path.append("/home/gbourdon/00_python_tools/packages")

'''def MerkAndPrins(phi, D, T_air, T_wall):
    """
    Compute the local Nusselt for natural convection of horizontal cylinder.
    Source : Merk And Prins (1954) Thermal convection in laminar boundary layers III, Appl.sci.Res
    :param xsi: angle in deg
    :return:
    """

    rho = 1.1700321
    cp = 1.0069629999999998 * 1000
    mu = 1.8367499999999997e-05
    k = 0.026151999999999998
    Pr = mu * cp / k

    Pr = 0.707
    A = 2 + 7 / 4 * Pr
    xsi = phi*np.pi/360 #from article

    DT = T_wall - T_air
    beta = 1/T_air
    def sn(n):
        if n == 1 :
            return 2
        else:
            return (-1)**n*2**(2*n)/(math.factorial(2*n+1))

    def H(xsi):

        h1 = sn(1)**.5
        h3 = A*sn(3)/(10*A+6)
        h5 = (A*sn(5)-(36*A+30)*h3**2)/(16*A+20)
        h7 = (A*sn(7) - (114*A+142)*h5*h3 - (54*A+42)*h3**3)/(22*A+42)
        h9 = (A*sn(9) - (156*A+264)*h7*h3 - (90*A +140)* h5**2 - (252*A+248)*h5*h3**2 - (27*A+18)*h3**4)/(28*A+72)

        return h1 *(xsi + h3*xsi **3 + h5*xsi**5 + h7*xsi**7 + h9*xsi**9)

    def dH(xsi):

        h1 = sn(1) ** .5
        h3 = A * sn(3) / (10 * A + 6)
        h5 = (A * sn(5) - (36 * A + 30) * h3 ** 2) / (16 * A + 20)
        h7 = (A * sn(7) - (114 * A + 142) * h5 * h3 - (54 * A + 42) * h3 ** 3) / (22 * A + 42)
        h9 = (A * sn(9) - (156 * A + 264) * h7 * h3 - (90 * A + 140) * h5 ** 2 - (252 * A + 248) * h5 * h3 ** 2 - (
                    27 * A + 18) * h3 ** 4) / (28 * A + 72)

        return h1*(1 + 3*h3 * xsi ** 2 + 5*h5 * xsi ** 4 + 7*h7 * xsi ** 6 + 9*h9 * xsi ** 8)
    temp =( 4/45 * Pr/ (Pr + 8/7))**(1/4)*dH(xsi)
    print(temp)
    return temp'''
D = 14/1000
rho = 1.1700321
cp = 1.0069629999999998 * 1000
mu = 1.8367499999999997e-05
nu = mu/rho
k = 0.026151999999999998
Pr = mu * cp / k
alpha = k/(rho*cp)
Tw = 310
T_air = 300
DT = Tw-T_air
beta = 1/Tw #perfect gas approximation
Ra = constants.g*beta*D**3*DT/(alpha*nu)
print(Ra)
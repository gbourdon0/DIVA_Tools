from modules.etude_param_config.adim_number import *


class FluidProperties:
    def __init__(self, rho, mu, k, cp, hfg, T, D=0, u=0):
        # properties
        self.rho = rho
        self.mu = mu
        self.cp = cp
        self.k = k
        self.hfg = hfg

        self.beta = 1 / T  # Warning : Assume perfect gas model
        # Conditions
        self.T = T
        self.D = D
        self.u = u

        # Adimensionnal number

        self.Pr = Pr(self.mu, self.cp, self.k)
        self.Re = Re(self.mu, self.D, self.u, self.rho)
        self.Ja_sup = None
        self.Ja_sub = None
        self.Gr = None

        # dictionnary
        self.adim_number = {
            "Pr": self.Pr,
            "Re": self.Re,
            "Ja_sub": self.Ja_sub,
            "Ja_sup": self.Ja_sup,
            "Gr": self.Gr
        }

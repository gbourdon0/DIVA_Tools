import numpy as np
class custom_fluid:
    """
    Class for the water properties. Follow the structure of the fluid_properties package
    """

    def __init__(self, **kwargs):
        # Init parent class
        self.k = np.nan
        self.cp = np.nan
        self.mu = np.nan
        self.rho = np.nan
        self.sigma = np.nan
        self.hfg = np.nan
        self.tsat = np.nan
        self.T = np.nan
        self.h = np.nan

        self.Pcr = np.nan
        self.Tcr = np.nan

        self.refresh()

        # Adimensionnal number

    # Adimensionnal number function
    def Re(self, v, D):
        return v * D * self.mu / self.rho

    def Ja_sub(self, Tl):
        if self.tsat - Tl:
            raise Exception(f"Tsat-Tl = {self.tsat - Tl} <0. Please check your input.")
        return self.cp * (self.tsat - Tl) / self.hfg

    def Ja_sup(self, Tw):
        if Tw - self.tsat:
            raise Exception(f"Tw - Tsat = {Tw - self.tsat} <0. Please check your input.")
        return self.cp * (Tw - self.tsat) / self.hfg

    # Refresh if needed
    def refresh(self):
        self.alpha = self.k / (self.rho * self.cp)
        self.Pr = self.mu * self.cp / self.k

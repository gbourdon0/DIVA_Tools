from iapws import IAPWS97


class Water(IAPWS97):
    """
    Class for the water properties. Follow the structure of the fluid_properties package
    """
    def __init__(self, **kwargs):
        # Init parent class
        kwargs["P"] = kwargs["P"] / 1e6  # convert in MPa for the IPAWS97 library
        IAPWS97.__init__(self, **kwargs)

        # Correct some variable to have in SI
        self.cp = self.cp * 1000  # Because it is in kJ in IAPWS97 .. bad
        self.h = self.h * 1000

        # Add some properties
        self.tsat = IAPWS97(P=self.P, x=0).T
        try:
            self.hfg = (IAPWS97(T=self.tsat, x=1).h - IAPWS97(T=self.tsat, x=0).h) * 1000
        except:
            pass
        self.Pcr = 22.09  # Mpa
        self.Tcr = 647.09  # K
        self.alpha = self.k / (self.rho * self.cp)

        # Adimensionnal number
        Pr = self.mu * self.cp / self.k

        # Adimensionnal number function
        def Re(v,D):
            return v*D*self.mu/self.rho
        def Ja_sub(Tl):
            if self.tsat-Tl:
                raise Exception(f"Tsat-Tl = {self.tsat-Tl} <0. Please check your input.")
            return self.cp*(self.Tsat-Tl)/self.hfg
        def Ja_sup(Tw):
            if Tw- self.tsat:
                raise Exception(f"Tw - Tsat = {Tw- self.tsat} <0. Please check your input.")
            return self.cp * (Tw - self.tsat) / self.hfg





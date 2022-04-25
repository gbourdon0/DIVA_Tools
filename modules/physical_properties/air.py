class air:
    """
    WARNING ! Only prop at 25 deg for now !!!
    """
    def __init__(self, temperature=25 + 273.15, pressure=0.1):
        self.temperature = temperature  # K
        self.pressure = pressure  # MPa


        self.rho = self.rho()
        self.cp = self.cp()
        self.mu = self.mu()
        self.k = self.k()
        self.beta = 1/self.temperature # perfect gas model
    @staticmethod
    def rho():
        return 1.1700321

    @staticmethod
    def cp():
        return 1.0069629999999998 * 1000

    @staticmethod
    def mu():
        return 1.8367499999999997e-05

    @staticmethod
    def k():
        return 0.026151999999999998
a = air()
print(a.cp,a.k,a.mu,a.rho)
import modules.diva_input as diva
from modules.fluid_properties.Custom_fluid import custom_fluid
import numpy as np

class DIVA_input:
    def __init__(self):
        self.paf = ""

    def load(self, path):
        self.paf = path
        self.TBC = diva.TBC()
        self.TBC.read_file(self.paf)
        self.NS = diva.NS()
        self.NS.read_file(self.paf)
        self.IC = diva.IC()
        self.IC.read_file(self.paf)
        self.MFBC = diva.MFBC()
        self.MFBC.read_file(self.paf)
        self.BC = diva.BC()
        self.BC.read_file(self.paf)
        self.PP = diva.PP()
        self.PP.read_file(self.paf)
        self.TSC = diva.TSC()
        self.TSC.read_file(self.paf)
        self.TP = diva.TP()
        self.TP.read_file(self.paf)

        # Create a fluid properties object
        self.liq = custom_fluid()
        self.liq.k = self.TP.kth_liq
        self.liq.cp = self.TP.cp_liq
        self.liq.mu = self.PP.mu_liq
        self.liq.rho = self.PP.rho_liq
        self.liq.tsat = self.TP.t_sat
        self.liq.sigma = self.PP.sigma
        self.liq.hfg = self.TP.hfg
        self.liq.T = self.IC.Tp_int
        self.liq.refresh()

        # Create a gas properties object
        self.gas = custom_fluid()
        self.gas.k = self.TP.kth_vap
        self.gas.cp = self.TP.cp_vap
        self.gas.mu = self.PP.mu_vap
        self.gas.rho = self.PP.rho_vap
        self.gas.tsat = self.TP.t_sat
        self.gas.sigma = self.PP.sigma
        self.gas.hfg = -self.TP.hfg
        self.gas.refresh()

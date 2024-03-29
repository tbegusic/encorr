import sys
import numpy as np
from utils.eq_corr import *

__all__ = ["NonEquilibrium"]


class NonEquilibrium(Equilibrium):

    """Implements difference between nonequilibrium expectation values of dipole under dipole perturbations with positive and negative fields.
       The result is <mu_{+}(t)> - <mu_{-}(t)>, which is related to the dipole-dipole correlation function and IR absorption spectra.
       The perturbation is assumed to be applied along the z axis.
    """

    def __init__(self, input_param):
        """Initialises base cell class.
        """
        super().__init__(input_param)
        self.epsilon = input_param.epsilon
        self.beta = input_param.beta

    def process(self):
        if 'dip' not in self.op:
            print('Only dipole moment nonequilibrium calculation implemented. op should be set to dip.')
            sys.exit()

        #Take only nonequilibrium part and only z component (perturbation is assumed to be along z axis).
        x = 0
        for bead in range(self.nbeads):
            x += np.loadtxt(self.sim_name + '.' + self.op + '_' + self.fmt_bead.format(bead))[self.nsteps1 + 1:, 2]
        x = x / self.nbeads
        c = 0
        corr = 0
        i_step = self.nsteps2 + 1
        for i in range(0, len(x), 2 * i_step):
            corr += x[i:i + i_step] - x[i + i_step : i + 2 * i_step]
            c+=1
        corr /= c * self.epsilon
        
        np.savetxt(self.out_name + self.op + '_neq_corr.dat', corr)


"""Class for equilibrium correlation functions.
"""

import numpy as np

__all__ = ["Equilibrium"]


class Equilibrium():

    """Implements equilbrium time correlation function for dipole and polarizability.

       Attributes:
    """

    def __init__(self, input_param):
        """Initialises base cell class.
        """
        self.sim_name = input_param.sim_name
        self.nbeads = input_param.nbeads
        self.op = input_param.op
        self.nsteps_total = input_param.nsteps_total
        self.nsteps_corr = input_param.nsteps_corr
        self.nsteps_shift = input_param.nsteps_shift

    def process(self):
        x = 0
        for bead in range(self.nbeads):
            x += np.loadtxt(self.sim_name + '.' + self.op + '_' + str(bead))
        x = x / self.nbeads

        if 'pol' in self.op:
            x = np.reshape(x, (len(x), 3, 3))
            for i in range(len(x)):
                x[i, range(3), range(3)] -= np.trace(x[i])/3
            corr_func = pol_aniso_corr
        else:
            corr_func = dipole_corr
                
        c = 0
        corr = np.zeros(self.nsteps_corr)
        for i in range(0, self.nsteps_total-self.nsteps_corr, self.nsteps_shift):
            corr_single = np.zeros(self.nsteps_corr)
            for j in range(self.nsteps_corr):
                corr_single[j] = corr_func(x[i], x[i + j])
            corr += corr_single
            c+=1
        corr = corr / c
        
        np.savetxt(self.op + '_eq_corr.dat', corr)
    

def dipole_corr(x1, x2):
    return np.dot(x1, x2)
def pol_aniso_corr(x1, x2):
    return np.trace(np.matmul(x1, x2))
def pol_iso_corr(x1, x2):
    return x1 * x2

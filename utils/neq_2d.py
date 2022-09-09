"""Class for equilibrium correlation functions.
"""

import sys
import numpy as np
from utils.neq_corr import *

__all__ = ["NonEquilibrium2D"]


class NonEquilibrium2D(NonEquilibrium):

    """Implements nonequilbrium expectation value of dipole.

       Attributes:
    """

    def __init__(self, input_param):
        """Initialises base cell class.
        """
        super().__init__(input_param)
        self.epsilon = input_param.epsilon
        self.field_pol = [ int(i) for i in input_param.field_pol.split(',') ]
        self.op = [ i.strip() for i in self.op.split(',') ]

    def process(self):
        x = []
        op_index = 0
        for op, field_pol in zip(self.op, self.field_pol):
            x_single = 0
            for bead in range(self.nbeads):
                if op_index == 0:
                    x_single += np.loadtxt(self.sim_name + '.' + op + '_' + self.fmt_bead.format(bead))[:self.nsteps1+1, field_pol]
                else:
                    x_single += np.loadtxt(self.sim_name + '.' + op + '_' + self.fmt_bead.format(bead))[self.nsteps1+1:, field_pol]
            op_index += 1
            x_single /= self.nbeads
            x.append(x_single)

        c = 0
        corr = 0
        i_step = self.nsteps2 + 1 #Number of steps for t1 and t2.
        for i in range(self.step1 + 1, len(x[0])+1, self.step1): #Start at the first available checkpoint from eq dynamics.
            if i >= i_step: #Check if we have enough dynamics to go backward -t1.
                #Backward equilibrium trajectory, first operator.
                eq = np.flip(x[0][i - i_step : i]) #Equilibrium dynamics part from time t (index i) to t-t1.
                #Difference between forward nonequilibrium trajectories, second operator.
                neq = x[1][2 * c * i_step : (2 * c + 1) * i_step] - x[1][(2 * c + 1) * i_step : 2 * (c + 1) * i_step] #Neq dynamics.
                #Compute corr[j, k] = eq[j] * neq[k].
                corr+=np.outer(eq, neq)
                c+=1
        corr *= self.beta / (c * self.epsilon)

        np.savetxt(self.out_name + self.op[0] + '_' + self.op[1] + '_neq_2d.dat', corr)


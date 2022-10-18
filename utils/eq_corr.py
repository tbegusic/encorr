import numpy as np

__all__ = ["Equilibrium"]


class Equilibrium():

    """Implements equilibrium time correlation function for dipole and polarizability.

       For dipole, it computes C(t) = <mu(0) .dot. mu(t)>, where .dot. denotes inner product. C(t) is related to the IR absorption spectrum.
       For polarizability, it computes C(t) = <Tr[beta(0) .dot. beta(t)]>, where beta = Pi - Id * Tr[Pi]/3, Pi is 3 x 3 polarizability tensor, 
       Id is 3 x 3 identity matrix, Tr is matrix trace, and .dot. is matrix-matrix product. C(t) is related to the anisotropic Raman spectrum.
    """

    def __init__(self, input_param):
        """Initialises base cell class."""
        self.sim_name = input_param.sim_name
        self.out_name = input_param.out_name
        self.nbeads = input_param.nbeads
        self.op = input_param.op
        self.nsteps1 = input_param.nsteps1
        self.nsteps2 = input_param.nsteps2
        self.step1 = input_param.step1
        self.step2 = input_param.step2

        self.fmt_bead = (
            "{0:0"
            + str(int(1 + np.floor(np.log(self.nbeads) / np.log(10))))
            + "d}"
        )

    def process(self):

        x = 0
        for bead in range(self.nbeads):
            x += np.loadtxt(self.sim_name + '.' + self.op + '_' + self.fmt_bead.format(bead))[:self.nsteps1+1]
        x = x / self.nbeads

        if 'pol' in self.op:
            x = np.reshape(x, (len(x), 3, 3))
            for i in range(len(x)):
                x[i, range(3), range(3)] -= np.trace(x[i])/3
            corr_func = pol_aniso_corr #Anisotropic Raman.
        else:
            corr_func = dipole_corr #IR absorption (dipole-dipole). 

        c = 0
        corr = np.zeros(self.nsteps2)
        for i in range(0, self.nsteps1 - self.nsteps2, self.step1):
            corr_single = np.zeros(self.nsteps2)
            for j in range(self.nsteps2):
                corr_single[j] = corr_func(x[i], x[i + j])
            corr += corr_single
            c+=1
        corr = corr / c
        
        np.savetxt(self.out_name + self.op + '_eq_corr.dat', corr)
    

def dipole_corr(x1, x2):
    return np.dot(x1, x2)
def pol_aniso_corr(x1, x2):
    return np.trace(np.matmul(x1, x2))

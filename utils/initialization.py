#!/usr/bin/env python3
import xml.etree.ElementTree as et

__all__ = ["Initializer"]

def read_xml(file_in):
  tree = et.parse(file_in)
  root = tree.getroot()
  return tree, root

class Initializer():

    @staticmethod
    def load_from_xml(file_in, file_in_spec):
        """Loads i-pi input file `file_in` and spectra-specific input file `file_in_spec` """
        #----------------------------
        #Spectra-specific parameters.
        #----------------------------
        tree, root = read_xml(file_in_spec)
        #Number of steps in the correlation function/nonequilibrium dynamics.
        try:
            nsteps2 = int(root.find('./corr_steps').text)
        except:
            nsteps2 = 1000
        #Number of steps for the window shift or number of steps between nonequilibrium trajectories.
        try:
            step1 = int(root.find('./step').text)
        except:
            step1 = 10
        # Read operators.
        try:
            op = root.find('./op').text
        except:
            op = 'dip'
        #Epsilon.
        try:
            epsilon = float(root.find('./epsilon').text)
        except:
            epsilon=0.1
        #Field polarization.
        try:
            field_pol = root.find('./field_pol').text
        except:
            field_pol = '0, 2'
        #Output file name.
        try:
            out_name = root.find('./output').text + '_'
        except:
            out_name = ''

        #----------------------------
        #I-PI input parameters.
        #----------------------------
        tree, root = read_xml(file_in)
        #Predix for the i-pi output files.
        try:
            sim_name = root.find('./output').attrib['prefix'] # Read simulation name.
        except:
            sim_name = 'simulation'
        #Number of beads.
        try:
            nbeads = int(root.find('./system/initialize').attrib['nbeads']) # Read number of beads.
        except:
            nbeads = 1
        #Stride for printing out dipole/polarizability values.
        try:
            for out in root.iter('trajectory'):
                if out.attrib['filename'] in op:
                    step2 = int(out.attrib['stride'])
        except:
            step2 = 1
        #Total number of equilibrium steps.
        try:
            nsteps1 = int(root.find('./total_steps').text)
        except:
            nsteps1 = 10000
        #Ensemble temperature in K converted to beta in atomic units.
        try:
            beta = float(root.find('./system/ensemble/temperature').text)
        except:
            beta = 300
        beta = 1.0 / (3.167e-6 * beta) #beta in atomic units.

        return Initializer(sim_name, nbeads, nsteps1//step2, nsteps2//step2, step1//step2, step2, op, epsilon, field_pol, beta, out_name)

    def __init__(self, sim_name, nbeads, nsteps1, nsteps2, step1, step2, op, epsilon, field_pol, beta, out_name):
        self.sim_name = sim_name
        self.nbeads = nbeads
        self.nsteps1 =  nsteps1
        self.nsteps2 = nsteps2
        self.step1 = step1
        self.step2 = step2
        self.op = op
        self.epsilon = epsilon
        self.field_pol = field_pol
        self.beta = beta
        self.out_name = out_name

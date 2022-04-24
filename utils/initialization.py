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
        #I-PI input parameters.
        #----------------------------
        tree, root = read_xml(file_in)
        try:
            sim_name = root.find('./output').attrib['prefix'] # Read simulation name.
        except:
            sim_name = 'simulation'
        try:
            nbeads = int(root.find('./system/initialize').attrib['nbeads']) # Read number of beads.
        except:
            nbeads = 1
        #----------------------------
        #Spectra-specific parameters.
        #----------------------------
        tree, root = read_xml(file_in_spec)
        #Total number of equilibrium steps.
        try:
            nsteps_total = int(root.find('./total_steps').text) 
        except:
            nsteps_total = 10000
        #Total number of equilibrium steps.
        try:
            nsteps_corr = int(root.find('./corr_steps').text)
        except:
            nsteps_corr = 1000
        #Total number of equilibrium steps.
        try:
            nsteps_shift = int(root.find('./shift_steps').text)
        except:
            nsteps_shift = 10
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

        return Initializer(sim_name, nbeads, nsteps_total, nsteps_corr, nsteps_shift, op, epsilon)

    def __init__(self, sim_name, nbeads, nsteps_total, nsteps_corr, nsteps_shift, op, epsilon):
        self.sim_name = sim_name
        self.nbeads = nbeads
        self.nsteps_total =  nsteps_total
        self.nsteps_corr = nsteps_corr
        self.nsteps_shift = nsteps_shift
        self.op = op
        self.epsilon = epsilon


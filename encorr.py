#!/usr/bin/env python3
import sys
import argparse

from utils.initialization import *
from utils.eq_corr import *
from utils.neq_corr import *
from utils.neq_2d import *

parser = argparse.ArgumentParser(description='Equilibrium and nonequilibrium correlation and response functions.')
parser.add_argument('--calc', default='eq', help='Type of calculation: eq, neq, or neq_2d.')
parser.add_argument('--input_ipi', default='input.xml', help='I-PI input xml file.')
parser.add_argument('--input_spec', default='input_spec.xml', help='Spectra-specific input xml file.')
args = parser.parse_args()

#Read from inputs.
init_param = Initializer.load_from_xml(args.input_ipi, args.input_spec)
#Set up calculation depending on calc command line input.
if args.calc=='eq': #Computes equilibrium correlation function.
    process = Equilibrium(init_param)
elif args.calc=='neq': #Computes nonequilibrium expectation value.
    process = NonEquilibrium(init_param)
elif args.calc=='neq_2d': #Computes two-dimensional equilibrium-nonequilibrium response function.
    process = NonEquilibrium2D(init_param)
else:
    print('Option --calc should be either eq, neq, or neq_2d.')
    sys.exit()
#Compute appropriate correlation.
process.process()

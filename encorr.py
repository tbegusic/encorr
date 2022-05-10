#!/usr/bin/env python3
import sys
import argparse

from utils.initialization import *
from utils.eq_corr import *
from utils.neq_corr import *
from utils.neq_2d import *

parser = argparse.ArgumentParser(description='Equilibrium and nonequilibrium correlations.')
parser.add_argument('--calc', default='eq', help='Type of calculation: eq, neq, or eq_neq.')
parser.add_argument('--input_ipi', default='input.xml', help='I-PI input xml file.')
parser.add_argument('--input_spec', default='input_spec.xml', help='Spectra-specific input xml file.')
args = parser.parse_args()

#Read from inputs.
init_param = Initializer.load_from_xml(args.input_ipi, args.input_spec)
#Set up calculation depending on calc command line input.
if args.calc=='eq':
    process = Equilibrium(init_param)
elif args.calc=='neq':
    process = NonEquilibrium(init_param)
elif args.calc=='neq_2d':
    process = NonEquilibrium2D(init_param)
else:
    print('Option --calc should be either eq, neq, or eq_neq.')
    sys.exit()
#Compute appropriate correlation.
process.process()

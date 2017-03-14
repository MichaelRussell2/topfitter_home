#! /usr/bin/env python

"""\
Check parameter space for most extremal values
"""
import random, os, math, shutil, glob
from math import sqrt
from sys import exit

import numpy as np

import optparse
op = optparse.OptionParser(usage=__doc__)
op.add_option("--param", dest="PARAM", type=str, default=None, help="Parameter to analyse")
opts, args = op.parse_args()

param_space = 'results_rebinned'
params = []

## TODO: Add observables other than cross-sections

dsize = len(os.walk(param_space).next()[1])
param_vals, param_errs = np.zeros(dsize), np.zeros(dsize)
for i in xrange(dsize):
    f = open(param_space+'/%03d/xsec.dat' % i , 'r')
    lines = f.readlines()
    param_vals[i], param_errs[i] = float(lines[0].split()[0]), float(lines[0].split()[0])
    
print "Max value of parameter xsec = %.03f. Found in directory %03d" % (param_vals.max(), param_vals.argmax())
print "Min value of parameter xsec = %.03f. Found in directory %03d" % (param_vals.min(), param_vals.argmin())

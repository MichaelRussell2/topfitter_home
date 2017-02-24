#! /usr/bin/env python

"""\
Check parameter space for most extremal values
"""
import random, os, math, shutil, glob
from math import sqrt
from sys import exit

import numpy as np

import optparse
op = optparse.OptionParser()
op.add_option("--param", dest="PARAM", type=str, default=None, help="Parameter to analyse")
opts, args = op.parse_args()

param_space = "param_space"
params = []

if not opts.PARAM:
    print "Choose a parameter to analyse"
    exit(1)

for ind, line in enumerate(open('param_space/000/used_params')):
    param = line.split()[0]
    params.append(param)
    if param == opts.PARAM: pind = ind

if opts.PARAM not in params:
    print "Parameter %s not defined. Available parameters are:" % opts.PARAM
    for ind, val in enumerate(params):
        print val
    exit(1)

dsize = len(os.walk("param_space").next()[1])
param_vals = np.zeros(dsize)
sq_dist = np.zeros(dsize)
for i in xrange(dsize):
    f = open('param_space/%03d/used_params' % i , 'r')
    lines = f.readlines()
    param_vals[i] += float(lines[pind].split()[1])
    float(lines[pind].split()[1])
    sq_dist[i] += sqrt(sum([float(x.split()[1])**2 for x in open('results/%03d/used_params' % i).readlines()]))
    
print "Max value of parameter %s = %.03f. Found in directory %03d" % (opts.PARAM, param_vals.max(), param_vals.argmax())
print "Min value of parameter %s = %.03f. Found in directory %03d" % (opts.PARAM, param_vals.min(), param_vals.argmin())
print "Closest point to the SM has Sqrt{Sum[C_i]} = %.03f. Found in directory %03d" % (sq_dist.min(), sq_dist.argmin())
print "Furthest point from the SM has Sqrt{Sum[C_i]} = %.03f. Found in directory %03d" % (sq_dist.max(), sq_dist.argmax())

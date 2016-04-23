#! /usr/bin/env python

"""\
Generate a randomly sampled parameter space.
"""
import random, os, math, shutil, glob

import optparse
op = optparse.OptionParser()
op.add_option("--ndim", dest="NDIM", type=int, default=6, help="dimensionality of parameter space to generate (default: %default)")
op.add_option("--npts", dest="NPTS", type=int, default=1000, help="number of sample points to generate (default: %default)")
op.add_option("--range", dest="BOUNDS", default="1e-1,1e3",help="boundaries of the parameter space (default: %default)")
op.add_option("--lin", dest="LIN", default=False, action="store_true", help="use linear spacing instead of logarithmic")

## TODO: Option to plot a 2D slice w/ mpl, to test randomness?

## Note: If you are fitting several different datasets together, you must use
##       the same parameter space for all of them.

opts, args = op.parse_args()

x_small, x_large = map(float, opts.BOUNDS.split(","))
lower, upper = math.log(x_small), math.log(x_large)

shutil.rmtree("param_space",ignore_errors='True')
os.mkdir("param_space")

for i in xrange(opts.NPTS):

    dname = os.path.join("param_space","%03d") % i
    os.mkdir(dname)

    ds, sws, cs = [], [], []
    for j in xrange(opts.NDIM):
        sws.append(random.choice([-1,1]))
        
        if (opts.LIN):
            ds.append(random.uniform(x_small, x_large))
            cs.append(sws[j]*ds[j])
        else:
            ds.append(random.uniform(lower, upper))
            cs.append(sws[j]*math.exp(ds[j]))
            
    f = open(dname + "/used_params", "w")
    for j in xrange(opts.NDIM):
        f.write("C%d  %.6g\n" % (j+1, cs[j]))
        

f.close()


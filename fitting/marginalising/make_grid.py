#! /usr/bin/env python

"""\
%prog [opts]

Set up a line of parameter points for a particular coefficient, to marginalise over the remaining parameters
"""
import sys, os, shutil, subprocess, re
from fileinput import FileInput as fp

import optparse
op = optparse.OptionParser(usage=__doc__)
op.add_option("--nstep", dest="NSTEP", type=int, default=201, help="number of points to calculate chi2 at (default=%default)")
op.add_option("--range", dest="BOUNDS", default="-1000,1000",help="boundaries of the hypercube")
op.add_option("--rundir", dest="RUNDIR", default="grid", help="name of directory where chi2s are stored (default=%default)")
opts, args  = op.parse_args()

low, high = map(int, opts.BOUNDS.split(","))
nstep = opts.NSTEP
rundir = opts.RUNDIR

shutil.rmtree(rundir,ignore_errors=True)
os.mkdir(rundir)

x = low
step = (high-low)/(nstep-1)

for j in xrange(nstep):

    dname = os.path.join(rundir,'%03d' % j )
    os.mkdir(dname)
    shutil.copy('marginal-ipol2chi2-1d',dname)
    f = os.path.join(dname,'marginal-ipol2chi2-1d')

    for line in fp(f, inplace=1):
        line = line.replace("-1000,1000", "%d,%d" % (low, high))
        line = line.replace("IX, X = 0, 0", "IX, X = %d, %d" % (j, x))

        print line,
    x+=step

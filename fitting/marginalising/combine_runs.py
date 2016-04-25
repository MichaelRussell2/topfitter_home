#!/usr/bin/env python

"""\
%prog [opts]

Paste together chi2s at different marginalising points along the 1D range for a given coefficient, extract marginalised 95% confidence limit at end
"""

import numpy as np
import os

import optparse
op = optparse.OptionParser(usage=__doc__)
op.add_option("--coeff", dest="COEFF", default="1", help="parameter to marginalise/slice in (default=%default)")
op.add_option("--rundir", dest="RUNDIR", default="grid", help="name of directory where chi2s are stored (default=%default)")
op.add_option("--cls", dest="CLS", default=False, action="store_true", help="output 95% confidence limits and best fit point for given coefficient")
opts, args = op.parse_args()

k = int(float(opts.COEFF))
rundir = opts.RUNDIR

path, dirs, files = os.walk(rundir).next()

N = len(dirs)
chi2s = 0
XC = []

NDF = 100 ## need to define this yourself

from scipy import stats as st

for i in xrange(len(dirs)):
    while i < N:
        chi2s+=np.loadtxt(os.path.join(rundir,'%03d','chi2s_min_6d_C%d.dat'),usecols=[1])  % (i, k)

    ## Use scipy to calculate 95% conf intervals, with ndf = nbins
    if (opts.CLS):
        cl = st.chi2.ppf(0.95, NDF)
        if (chi2 < cl ):
            XC.append(X)

Xmin =  low+step*np.argmin(chi2s)
chi2min = np.min(chi2s)

if (opts.CLS):
    print
    print 'RAW CHI2 LIMITS:'        
    print '95%% c.l. on coefficient C = (%.f, %.f)' % (XC[0], XC[-1])
    print 'Best fit point at C = %.f' % Xmin

np.savetxt("chi2s_%dd_%s.dat" % (NOPS, paramidstr), chi2s.T, fmt="%.10f")        

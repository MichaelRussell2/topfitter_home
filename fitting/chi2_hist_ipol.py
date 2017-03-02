#! /usr/bin/env python2.7

"""\
%prog <datadir>

Calculate interpolated chi2 per histogram at a given point in parameter space
"""
import optparse
op = optparse.OptionParser(usage=__doc__)
op.add_option("--ifile", dest="IFILE", default="ipol.dat", help="file from which to read the bin interpolations (default: %default)")

opts, args = op.parse_args()
DATADIR = args[0]

import professor2 as prof
import numpy as np
import math

## Load interpolated histograms from file
IMETA = prof.read_meta(opts.IFILE)
IHISTOS = prof.read_binnedipol(opts.IFILE)
HNAMES = IHISTOS.keys()
#print sorted(HNAMES)

## Extract parameter info from ipol file
PARAMNAMES = IMETA["ParamNames"].split()
NOPS = len(PARAMNAMES)

## Read reference data histos
import os, glob
DHISTOS = {}
reffiles = glob.glob(os.path.join(DATADIR, "ref", "*"))
for rf in reffiles:
    DHISTOS.update(prof.read_histos(rf))
## Remove /REF prefixes
DHISTOS = { p.replace("/REF", "") : h for (p, h) in DHISTOS.iteritems() }

def chi2_hist(ihist, dhist, params):
    assert len(ihist.bins) == len(dhist.bins)
    chi2, ndf = 0.0, 0
    covmatfile = DATADIR+ "/corr/" + dhist.path.replace("/", "_").replace("REF","").strip("_") + ".dat"
    if os.path.exists(covmatfile): 
        covmat = np.loadtxt(covmatfile) 
    else:
        covmat = np.identity(len(ihist.bins))
    chi2_bs, y_bs, ey_bs = [], [], []
    for nb1, (ib1, db1) in enumerate(zip(ihist.bins, dhist.bins)):
        for nb2, (ib2, db2) in enumerate(zip(ihist.bins, dhist.bins)):
            if (nb1 <= nb2):
                cov12 = covmat[nb1,nb2]
                ival1, ival2 = ib1.val(params), ib2.val(params)
                dy1, dy2  = ival1 - db1.val, ival2 - db2.val
                ierr1, ierr2 = ib1.err(params), ib2.err(params)
                ipolerr1, ipolerr2 = 0.03*ival1, 0.03*ival2
                derr1, derr2 = db1.err, db2.err
                ey12, ey22 = derr1**2 + ierr1**2 + ipolerr1**2,  derr2**2 + ierr2**2 + ipolerr2**2
                ey2 = math.sqrt(ey12*ey22)
                if (dy1 and not ey2):# or (dy2 and not ey2):
                    print "WARNING: Zero error for non-zero bin in chi2 calculation for %s:%d. Skipping..." % (ihist, nb)
                    continue
                if (ey2):
                    chi2_b = dy1*cov12*dy2/ey2
                    chi2 += chi2_b
                    chi2_bs.append(chi2_b)
            else:
                #print "Already counted this bin pair once!"
                continue
    
        ndf += 1
    return chi2, ndf



## Plot interpolations at a fixed position
PARAMPT = [0 for _ in xrange(NOPS)] # SM

from matplotlib import pyplot as pl
chi2_total, ndf_total = 0.0, 0
for h in sorted(HNAMES):
    print
    print h
    dhist = DHISTOS[h]
    ihist = IHISTOS[h]
    chi2_h, ndf_h = chi2_hist(ihist, dhist, PARAMPT)
    print "chi2_hist, ndf_hist, chi2_per_ndf_hist =", chi2_h, ndf_h, chi2_h/ndf_h
    chi2_total += chi2_h
    ndf_total += ndf_h
    #

print
print "Total chi2 = %f for %d degrees of freedom" %  (chi2_total, ndf_total)

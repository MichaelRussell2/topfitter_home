#! /usr/bin/env python

"""\
Calculate raw chi2 between data and mc histograms at sample point
"""
import random, os, math, shutil, glob, sys
from math import sqrt
import numpy as np

if len(sys.argv)!=2:
    print "Enter parameter space directory as argument"
    sys.exit()

mcpoint = sys.argv[1]        
PARAMPT = [float(x.split()[1]) for x in open('param_space/%s/used_params' % mcpoint).readlines()]
print PARAMPT

datadir = 'data'
mcroot = 'results_rebinned'
mcdir = os.path.join(mcroot,mcpoint)

histos = os.walk(datadir).next()[2]

## switch for multi-bin histo (T) or 1-bin observable (F)
diff = True

for histo in histos:
#    if 'mtt' in histo or 'absytt' in histo: continue 
    print "observable:", histo #.upper()
    chi2_hist, ndf_hist = 0., 0
    mc_file = os.path.join(mcdir,histo)
    data_file = os.path.join(datadir,histo)
    if diff:
        xlo, xhi, ymc, dymc = np.loadtxt(mc_file,unpack=True)
        xlo, xhi, yda, dyda = np.loadtxt(data_file,unpack=True)
        assert len(ymc) == len(yda)
        print 'Bin:\t', 'chi2:'
        for i, y in enumerate(ymc):
            chi2_bin = (ymc[i]-yda[i])**2/(dymc[i]**2+dyda[i]**2)
            print i, '\t', chi2_bin
            chi2_hist += chi2_bin
            ndf_hist += 1
    else:
        ymc, dymc = np.loadtxt(mc_file,unpack=True)
        yda, dyda = np.loadtxt(data_file,unpack=True)
        print ymc, yda
        print dymc, dyda
        chi2_bin = (ymc-yda)**2/(dymc**2+dyda**2)
        ndf_hist += 1
    
    print 'total chi2:', chi2_hist, 'for', ndf_hist, 'bins\n'

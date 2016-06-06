#! /usr/bin/env python

"""\
Muliply leading order histograms with K-factors
K-factors must be in kfactors/ directory 
Input files have form x y dy (dy is taken as zero)
K-factors files have x y dy dy/y
Output files x y dy
"""

import sys, os, shutil

import optparse
op = optparse.OptionParser()
opts, args = op.parse_args()

indir="results"
kdir="kfactors"
outdir="results_reweighted"
shutil.rmtree(outdir,ignore_errors=True)
os.mkdir(outdir)

dsize = len(os.walk(indir).next()[1])

import numpy as np
for i in xrange(dsize):
    os.mkdir(os.path.join(outdir,"%03d" %i))
    shutil.copy(os.path.join(indir,"%03d" %i,"used_params"),os.path.join(outdir,"%03d" %i))

    for infile in args:
        ys_lo=np.loadtxt(os.path.join(indir,"%03d" %i ,infile),usecols=(0,1) )
        kfile=outfile=infile
        ks=np.loadtxt(os.path.join(kdir,kfile),usecols=(0,1,2,3))
        xs=ys_lo[:,0]
        assert len(ys_lo[:,1])==len(ks[:,1])
        ys_nlo=ys_lo[:,1]*ks[:,1]
        ys_nlo_err=ys_nlo*ks[:,3]
        np.savetxt(os.path.join(outdir,"%03d" %i,outfile),np.c_[xs,ys_nlo,ys_nlo_err], fmt="%.5f")
        
    

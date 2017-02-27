#! /usr/bin/env python

"""\
Muliply leading order histograms with K-factors
K-factors must be in kfactors/ directory 
Input files have form xlo xhi y dy (dy is taken as zero)
K-factors files have xcent y dy or xlo xhi y dy
Output files xlo xhi y dy
"""

import sys, os, shutil, glob

import optparse
op = optparse.OptionParser()
opts, args = op.parse_args()

indir="results"
kdir="kfactors"
outdir="results_reweighted"
shutil.rmtree(outdir,ignore_errors=True)
os.mkdir(outdir)

dsize = len(os.walk(indir).next()[1])-1
import numpy as np
for i in xrange(dsize):
    infiles = glob.glob(os.path.join(indir,"%03d" %i ,'*.dat'))
    os.mkdir(os.path.join(outdir,"%03d" %i))
    shutil.copy(os.path.join(indir,"%03d" %i,"used_params"),os.path.join(outdir,"%03d" %i))

    for infile in infiles:
        x_min, x_max, y_lo  = np.loadtxt(infile,usecols=(0,1,2),unpack=True)

        kfile=outfile=infile.split('/')[-1]
        ks=np.loadtxt(os.path.join(kdir,kfile),usecols=None)
        ks_nrows, ks_ncols = ks.shape[0], ks.shape[1]

        assert len(y_lo) == ks_nrows 
        if ks_ncols == 3:
            y_nlo=y_lo*ks[:,1]
            y_nlo_err=y_nlo*ks[:,2]
        elif ks_ncols == 4:
            y_nlo=y_lo*ks[:,2]
            y_nlo_err=y_nlo*ks[:,3]
        np.savetxt(os.path.join(outdir,"%03d" %i, outfile),np.c_[x_min,x_max,y_nlo,y_nlo_err], fmt="%.5f")

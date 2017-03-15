#! /usr/bin/env python

"""\
Muliply leading order histograms with K-factors
K-factors must be in kfactors/ directory 
Input files have form xlo xhi y dy (dy is taken as zero)
K-factors files have xcent y dy or xlo xhi y dy
Output files xlo xhi y dy
"""

import sys, os, shutil, glob
import numpy as np

indir="results"
kdir="kfactors"
outdir="results_reweighted"

def main():
    shutil.rmtree(outdir,ignore_errors=True)
    os.mkdir(outdir)

    dsize = len(os.walk(indir).next()[1])
    for i in xrange(dsize):
        infiles = glob.glob(os.path.join(indir,"%03d" %i ,'*.dat'))
        os.mkdir(os.path.join(outdir,"%03d" %i))
        shutil.copy(os.path.join(indir,"%03d" %i,"used_params"),os.path.join(outdir,"%03d" %i))

        for infile in infiles:
            fname = os.path.basename(infile)
            outfile = os.path.join(outdir,"%03d" %i,fname)
            nlo_rw(infile,outfile)

def nlo_rw(histo,outfile):

    if np.loadtxt(histo,usecols=None).shape[0] > 2:
        x_min, x_max, y_lo  = np.loadtxt(histo,usecols=(0,1,2),unpack=True)

        kfile=os.path.join(kdir,os.path.basename(histo))
        ks=np.loadtxt(kfile,usecols=None)
        ks_nrows, ks_ncols = ks.shape[0], ks.shape[1]

        assert len(y_lo) == ks_nrows 
        if ks_ncols == 3:
            y_nlo=y_lo*ks[:,1]
            y_nlo_err=y_nlo*ks[:,2]
        elif ks_ncols == 4:
            y_nlo=y_lo*ks[:,2]
            y_nlo_err=y_nlo*ks[:,3]
        np.savetxt(outfile,np.c_[x_min,x_max,y_nlo,y_nlo_err], fmt="%.5f")

    elif np.loadtxt(histo,usecols=None).shape[0] == 2:
        y_lo, dy_lo  = np.loadtxt(histo,usecols=(0,1),unpack=True)
        kfile=os.path.join(kdir,os.path.basename(histo))
        ks=np.loadtxt(kfile,usecols=None)
        y_nlo=y_lo*ks[0]
        y_nlo_err=y_nlo*ks[1]

        np.savetxt(outfile,np.c_[y_nlo,y_nlo_err], fmt="%.5f")

if __name__ == "__main__":
    main()

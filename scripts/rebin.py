#!/usr/bin/env python

import os, shutil, glob
import numpy as np
from math import sqrt

indir='results_reweighted'
datadir='data'
outdir='results_rebinned_test'

# TODO: Deal with overflow/underflow

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
            rebin(infile,outfile)
    

def rebin(histo,outfile):
    xlo, xhi, y, yerr = np.loadtxt(histo,unpack=True)

    datafile = os.path.join(datadir,os.path.basename(histo))
    xlo_dat, xhi_dat, y_dat, yerr_dat = np.loadtxt(datafile,unpack=True)

    oldbins = np.append(xlo, xhi[-1])
    newbins = np.append(xlo_dat,xhi_dat[-1])
    if any([ x not in oldbins for x in newbins]) and '000' in histo:
        print "Warning: New bins are not subset of old bins for file %s." % os.path.basename(histo)
        print "         May get undefined behaviour."

    y_rebin = np.zeros(len(newbins)-1)
    dy_rebin = np.zeros(len(newbins)-1)

    BinWidth, Normalize, scale = True, True, 1e3

    rect, height, height_err = 0, 0, 0
    integral = y.sum()

    for i, val in enumerate(xhi):
        rect += y[i]*abs(xhi[i]-xlo[i])
        height += y[i]
        height_err += yerr[i]**2
        if val in newbins:
            ind_rb = int(np.where(newbins==val)[0])
            width = abs(newbins[ind_rb]-newbins[ind_rb-1])
            y_rebin[ind_rb-1] += height
            dy_rebin[ind_rb-1] += sqrt(height_err)
            if Normalize:
                y_rebin[ind_rb-1] /= integral
                dy_rebin[ind_rb-1] /= integral
            if BinWidth:
                y_rebin[ind_rb-1] /= width
                dy_rebin[ind_rb-1] /= width
            y_rebin[ind_rb-1] *= scale
            dy_rebin[ind_rb-1] *= scale
            rect, height, height_err = 0, 0, 0
#        print

    np.savetxt(outfile, np.c_[xlo_dat, xhi_dat, y_rebin, dy_rebin], fmt=['%.1f\t','%.1f\t','%.5f\t','%.5f\t'])
    
if __name__ == "__main__":
    main()






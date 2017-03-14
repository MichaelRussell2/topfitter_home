#! /usr/bin/env python

"""\
Convert xsec/bin to nevents/bin and add in corresponding statistical error 
Input files have form xlow xhigh y dy or y dy
Output files xlow xigh y dy_sys dy_stat (symmetric error by construction)
"""

import sys, os, shutil, glob
import numpy as np

if (len(sys.argv) !=3):
    print 'Give int. luminosity in fb^-1 and systematic uncertainty in %'
    sys.exit()
lumi, syst = sys.argv[1], sys.argv[2]

print "Using integrated luminosity of %s inverse fb and systematic uncertainty of %s %%" % (lumi, syst) 
lumi, syst = float(lumi), float(syst)

indir_mc='results_reweighted'
indir_data='data'
outdir_mc='events_mc'
outdir_data='events_data'

def main():

    ## tidy up old runs
    for outdir in outdir_mc, outdir_data:
        shutil.rmtree(outdir,ignore_errors=True)
        os.mkdir(outdir)

    ## convert mc histos from xsec/bin -> nevts/bin
    dsize=len(os.walk(indir_mc).next()[1])
    for i in xrange(dsize):
        infiles = glob.glob(os.path.join(indir_mc,"%03d" %i ,'*.dat'))
        os.mkdir(os.path.join(outdir_mc,"%03d" %i))
        shutil.copy(os.path.join(indir_mc,"%03d" %i,"used_params"),os.path.join(outdir_mc,"%03d" %i))

        for infile in infiles:
            fname = os.path.basename(infile)
            outfile = os.path.join(outdir_mc,"%03d" %i,fname)
            scalebylumi(infile,outfile)

    ## convert data or pseudodata histos from xsec/bin -> nevts/bin
    infiles_data=glob.glob(os.path.join(indir_data,'*.dat'))
    for infile in infiles_data:
        fname = os.path.basename(infile)
        outfile = os.path.join(outdir_data,fname)
        scalebylumi(infile,outfile)


        
def scalebylumi(histo,outfile):

    ## Need either 2 columns or 4 columns of input data
    if np.loadtxt(histo,usecols=None).shape[0] == 4:
        xlo, xhi, y_xsec, dy_xsec = np.loadtxt(histo,unpack=True)
    elif np.loadtxt(histo,usecols=None).shape[0] == 2:
        y_xsec, dy_xsec= np.loadtxt(histo,unpack=True)
        xlo, xhi = 0, 0
    else:
        print 'Bad input data format in file %s. Exiting' % histo
        sys.exit()

    ## xsec in pb: convert lumi to pb^-1
    lumipb = lumi*1000
    
    y_evts = y_xsec*lumipb 
    dy_evts_stat = np.sqrt(y_evts)
    if 'data' in histo:
        ## experimental syst
        dy_evts_sys = y_evts*syst/100 
    else:
        ## theory syst
        dy_evts_sys = dy_xsec*lumipb
        # dy_evts_sys = dy_xsec*0 ##no theory uncertainty
    dataFMT=['%.1f\t','%.1f\t','%.5f\t','%.5f\t','%.5f\t']
    np.savetxt(outfile,np.c_[xlo, xhi, y_evts, dy_evts_sys, dy_evts_stat],fmt=dataFMT)

if __name__ == "__main__":
    main()

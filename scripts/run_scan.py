#! /usr/bin/env python
"""\
%prog [opts]

Start running MadEvent samples in series (see make_batch_grid.py for parallel options)
Requires as input:
 * 'param_space' directory with numbered subdirectories and used_params file in each subdir
 * 'samples' directory with MadEvent stuff: bin, source, subprocesses etc.
 * 'param_card_sm.dat' : default (SM) parameter card for MadEvent
 * if analysing events with FastPartons, subdir of samples called 'Analysis' with FastPartons src
"""

import os, shutil, re, fileinput, glob
from subprocess import call
from sys import exit, stderr

import optparse
op = optparse.OptionParser(usage=__doc__)

op.add_option("--xsec",dest="XSEC", default=False, action="store_true", help="Get total cross-section only, no event plotting.")
op.add_option("--npts",dest="NSCAN", default=1000, type=int,help="number of scan points")
op.add_option("--nevts",dest="NEVTS", default=100000, type=int,help="number of events per run")
op.add_option("--info",dest="INFO", default=False, action="store_true", help="Print additional parameterinfo.")

opts, args = op.parse_args()

maindir=os.getcwd()

## make results directories
dirs=["results","samples/outputs","samples/Events"]
for d in dirs:
    shutil.rmtree(d,ignore_errors=True)
    os.mkdir(d)
outdir=os.path.join(maindir,"results")

## get number of parameter space points
size=opts.NSCAN 
param_space = 'param_space'
dsize = len(os.walk(param_space).next()[1])
if size > dsize:
    print "Number of requested points exceeds number of available param space points. Exiting"
    exit(1)

## operators in model parameter card to scan
#ops=["ReCuW33","ReCuB33","ReC3Phiq33","ReC1Phiq33","ReCPhiu33"]
ops=["CG","ReCuG33","C1qq1331","C8qu3311","C3qq1331","C8ud3311"]

def main():

    ## start running MadEvent samples
    for i in xrange(size):
        dname = "results/%03d" % i
        os.mkdir(dname)
        shutil.copy(os.path.join(param_space,'%03d' % i, 'used_params'),dname)
    
        ## write parameter space point to list
        cs = []
        for ind, line in enumerate(open(param_space+'/%03d/used_params' % i )):
            cs.append(line.split()[1])
            cs[ind] = float(cs[ind])
        
        print 'At run %03d' % i
        banner = 'samples/outputs/' + 'output%03d' %i 

        if i==1:
            import datetime
            start=datetime.datetime.now()

        ## generate samples at param space point
        run_point(cs,banner)
        extract_xsec(banner,os.path.join(maindir,dname,'xsec.dat'))

        ## (optionally) analyse events using FastPartons
        evts = os.path.join('samples','Events','run_01','unweighted_events.lhe.gz')
        if not opts.XSEC:
            analyse_point(i, evts, os.path.abspath(dname))

        shutil.rmtree('samples/Events/run_01')

        if i==1:
            elapsed=datetime.datetime.now()
            totdur = (opts.NSCAN-1)*((elapsed-start))
            print "%d runs requested. Estimated finish time:" % opts.NSCAN
            print (start+totdur).ctime()
            print

def run_point(PARAMPT,runlog):
    f = os.path.join('samples','Cards','param_card.dat')
    shutil.copy('param_card_sm.dat', f)

    ## check dimensionality
    try:
        assert len(PARAMPT)==len(ops)        
    except:
        stderr.write("Number of operators must match dimensionality of parameter space. Exiting\n")
        exit(1)

    ## replace SM param_card.dat with values of operators 
    for line in fileinput.FileInput(f,inplace=1):
        for j in xrange(len(ops)):
            line = line.replace("0e-08 # %s " % ops[j], "%fe-08 # %s " % (PARAMPT[j], ops[j]))
        print line,
    for line in fileinput.FileInput(os.path.join('samples','Cards','run_card.dat'),inplace=1):
        line = line.replace("100000 = nevents", "%d = nevents" % opts.NEVTS )
        print line,

    ## generate events, redirect MadEvent output 
    print 'Generating events'
    outstream = open(runlog, 'w')
    call(["./samples/bin/generate_events","-f"], stdout=outstream )
    outstream.close()
    print 'Done'


def extract_xsec(runlog,outfile):

    ## read cross-section from MadEvent output
    for line in open(runlog,"r"):
        if re.match("(.*)Cross-section(.*)", line):
            xsec = float(line.split()[2])
            xsec_err = float(line.split()[4]) 

            ## write cross-section to file           
            with open(outfile, 'w') as fout:
                fout.write('%g  %g\n' % (xsec, xsec_err))
                fout.close()

def analyse_point(i,evtfile,outdir):
    
    shutil.move(evtfile,'samples/Analysis')
    os.chdir('samples/Analysis')
    
    ## compile analysis on first run
    if i==0:
        print "Building FastPartons"
        try:
            assert(call(["make"],stdout=open(os.devnull, 'wb')) == 0)
            print "Done"
        except:
            stderr.write("Failed to build FastPartons. Exiting\n")
            exit(1)

    ## plot events and delete after plotting
    call(["gunzip","unweighted_events.lhe.gz"])
    call(["./analysis", "unweighted_events.lhe" ])
    os.remove("unweighted_events.lhe")
    infiles = glob.glob("*.dat")

    ## check binning is same as kfactors
    if i==0:
        import numpy as np
        for infile in infiles:
            npinfile = np.loadtxt(infile)
            try:
                kfile = np.loadtxt(os.path.join(maindir,"kfactors",infile))
                assert len(npinfile) == len(kfile)
                ans='y'
            except AssertionError:
                ans=raw_input("Warning: k-factor binning mismatch for %s. Continue anyway? (y/n) " % infile)
            except IOError:
                ans=raw_input("Warning: no k-factors for %s. Continue anyway? (y/n) " % infile)
            if ans.lower()== ('y'):
                continue
            else: exit(1)

    ## copy histograms over to results directory
    [shutil.copy(f,outdir) for f in infiles]
    os.chdir(maindir)

if __name__ == "__main__":
    main()

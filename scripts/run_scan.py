#! /usr/bin/env python
"""\
%prog [opts]

Start running MadEvent samples in series (see make_batch_grid.py for parallel options) 
"""

import os, shutil, re, fileinput
from subprocess import call
from sys import exit

import optparse
op = optparse.OptionParser(usage=__doc__)

op.add_option("--xsec",dest="XSEC", default=False, action="store_true", help="Get total cross-section only, no event plotting.")
op.add_option("--npts",dest="NSCAN", default=1000, help="number of scan points")
#op.add_option("--parallel",dest=BATCH, default=False, action="store_true", help="Generate a grid of sample points to run in parallel.")
#op.add_option("--ncoeff",dest=NCOEFF, default=6, help="Check dimensionality of parameter space is same as ")

opts, args = op.parse_args()

main=os.getcwd()

dirs=["plots","results","samples/outputs","samples/Events"]
for d in dirs:
    shutil.rmtree(d,ignore_errors=True)
    os.mkdir(d)
outdir=os.path.join(main,"plots")
    
size=opts.NSCAN 
dsize = len(os.walk("param_space").next()[1])
if size > dsize:
    print "Number of requested points exceeds number of available param space points. Exiting"
    exit(1)

for i in xrange(size):
    dname = "results/%03d" % i
    os.mkdir(dname)
    f = os.path.join('samples','Cards','param_card.dat')
    shutil.copy('param_card_sm.dat', f)

    cs = []
    for ind, line in enumerate(open('param_space/%03d/used_params' % i )):
        cs.append(line.split()[1])
        cs[ind] = float(cs[ind])

    ops=["CG","ReCuG33","C1qq1331","C8qu3311","C3qq1331","C8ud3311"]
    assert len(cs)==len(ops)        

    for line in fileinput.FileInput(f,inplace=1):
        for j in xrange(len(ops)):
            line = line.replace("0e-08 # %s " %ops[j], "%fe-08 # %s " % (cs[j], ops[j]))
        print line,

    os.chdir('samples')
    g=open('outputs/' + 'output%03d' %i , 'w' )
    call(["./bin/generate_events","-f"], stdout=g )

    if not opts.XSEC:
        evtfile=os.path.join('Events','run_01','unweighted_events.lhe.gz')
        if os.path.exists(evtfile):
            print 'At run %03d' % i
            shutil.move(evtfile,'MadAnalysis')
            os.chdir('MadAnalysis')
            call(["gunzip","unweighted_events.lhe.gz"])
            call(["./plot_events"],stdout=open(os.devnull, 'wb'))
            os.remove("unweighted_events.lhe")
            shutil.copy('plots.top', os.path.join(outdir,'plots%03d.top') % i )
        else:
            print 'Events were not generated for run %03d' % i

    os.chdir(main)
    shutil.rmtree('samples/Events/run_01')

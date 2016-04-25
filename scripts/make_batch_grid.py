#! /usr/bin/env python

"""\
%prog [opts]

Create a grid of MadEvent directories to generate multiple runs in parallel 
"""

import os, shutil, re, fileinput
from subprocess import call
from sys import exit

import optparse
op = optparse.OptionParser(usage=__doc__)

op.add_option("--npts",dest="NSCAN", default=1000, help="number of scan points (default=%default)")

opts, args = op.parse_args()

main=os.getcwd()

dirs=["plots","results","samples/outputs","samples/Events","runs"]
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
    dname = "runs/%03d" % i
    shutil.copytree('samples',dname)
    f = os.path.join(dname,'Cards','param_card.dat')
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

    os.chdir(main)

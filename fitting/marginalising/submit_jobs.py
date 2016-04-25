#! /usr/bin/env python

import sys, os
from subprocess import call

import optparse
op = optparse.OptionParser()

op.add_option("--rundir", dest="RUNDIR", default="grid", help="name of directory where chi2s will be stored (default=%default)")
op.add_option("--queue", dest="QUEUE", default="medium6", help="PBS queue to submit jobs to (default=%default)")
op.add_option("--jobname", dest="JOBNAME", default="marginal-ipol2chi2-1d", help="name of job file to run on farm (default=%default)")
opts, args = op.parse_args()

queue = opts.QUEUE
rundir = opts.RUNDIR
jobname = opts.JOBNAME

dirs = os.walk(rundir).next()[1]


jobargs = "data+MCdirectories"
jobargs += ""

for dirname in dirs:
    call(["qsub","-q",queue,"-d",dirname,"-F",jobname,jobargs], stdout=g )

#! /usr/bin/env python

"""\
%prog <directory_name> [opts]

Initialise a topfitter dataset directory.
"""
import os, shutil, glob, sys
import textwrap
from sys import exit

import optparse
op = optparse.OptionParser(usage=__doc__)
op.add_option("--proc", dest="PROCESS", default=None, help="Process to generate (default=%default)")
op.add_option("--coll", dest="COLLIDER", default=None, help="Collider settings to use. For advanced options edit the card yourself (default=%default)")
op.add_option("--mod", dest="MODEL", default="warsaw_d6", help="New physics model to test (default=%default)")
op.add_option("--dat", dest="DATASET", default=None, help="arXiv code of dataset to fit to, see list (default=%default)")
op.add_option("--list-datasets", dest="LIST", default=False, action="store_true", help="List available measurements to fit to and quit")
op.add_option("--list-processes", dest="LISTPROCS", default=False, action="store_true", help="List available processes and quit")
op.add_option("--filter", dest="FILTER", default=None,help="Filter available measurements by various settings (also see list-filters)")
op.add_option("--xsec", dest="XSEC", default=False, action="store_true", help="Cross-sections only, no event plotting")
op.add_option("--batch", dest="BATCH", default=False, action="store_true", help="Generate different MC runs in parallel on a batch farm")

opts, args = op.parse_args()

database="datasets"
path, datasets, files = os.walk(database).next()

## list available processes   
if (not args and opts.LISTPROCS):
    sys.path.append('dictionary')
    from processes import dictionary as p_d
    print
    print "Process:  Description\n"
    for key, val in p_d.iteritems():
        print "\t%s   %s" % (key, val)
    exit(0)


## list available measurements and/or filter by collider/process 
if (not args and opts.LIST and not opts.FILTER ):
    print "Possible measurements to fit to:\n"
    for d in datasets:
        with open(os.path.join(database,d,"TAG"),'r') as tag:
            tag=tag.read()
        print '\t%s: %s' % (d, tag)
    exit(0)    
elif (not args and opts.LIST and opts.FILTER ):
    print "Measurements matching %s:\n" % opts.FILTER
    if "," in opts.FILTER:
        filters = opts.FILTER.split(",")
        for d in datasets:
            if all(filt in open(os.path.join(database,d,'settings')).read() for filt in filters):
                with open(os.path.join(database,d,"TAG"),'r') as tag:
                    tag=tag.read()
                print '\t%s: %s' % (d, tag)
        exit(0)
    else:
        for d in datasets:
            if (opts.FILTER) in open(os.path.join(database,d,'settings')).read():
#            if (opts.FILTER.upper() or opts.FILTER.lower()) in open(os.path.join(database,d,'settings')).read():
                with open(os.path.join(database,d,"TAG"),'r') as tag:
                    tag=tag.read()
                print '\t%s: %s' % (d, tag)
#                print '\t%s: %s'  % (d, '\n\t\t'.join(textwrap.wrap(tag, 80, break_long_words=False)) )
        exit(0)
elif not args and not opts.LIST:
    op.print_help()
    exit(1)
elif args and not opts.PROCESS:
    print "Must choose a process type for the fit directory (see --list-processes option)"
    exit(1)
elif args and not opts.COLLIDER:
    print "Must choose a collider type for the fit directory"
    exit(1)
elif args and not opts.DATASET:
    print "Must choose a dataset to fit to (see --list-datasets option)"
    exit(1)    
elif len(args)>1:
    print "Too many arguments. Exiting"
    exit(1)    

## initialise output directory    
OUTDIR=args[0]
if os.path.exists(OUTDIR):
    ans = raw_input("%s already exists. Overwrite this directory? (y/n)\n" % OUTDIR)
    if ans.lower() == ('y'):
        shutil.rmtree(OUTDIR,ignore_errors=True)
        os.mkdir(OUTDIR)
    else:
        print "Exiting"
        exit(0)

## index process/collider options
processes=os.walk("processes").next()[2]
colliders=os.walk("colliders").next()[2]
models=os.walk("models").next()[2]

processes = [f.split(".")[0] for f in processes]

## check if options available    
if not opts.PROCESS in processes:
    print "Not in available processes"
    exit(1)
if not opts.COLLIDER in colliders:
    print "These collider settings aren't available"
    exit(1)
if not opts.DATASET in datasets:
    print "Measurement not available"
    exit(1)
if not opts.MODEL in models:
    print "This model not yet available"
    exit(1)    

## data to fit to
dataset=opts.DATASET
shutil.copytree(os.path.join(database,dataset,"bins"),os.path.join(OUTDIR,"data"))
if os.path.isdir(os.path.join(database,dataset,"corrs")):
    shutil.copytree(os.path.join(database,dataset,"corrs"),os.path.join(OUTDIR,"correlations")) 
    
## check if settings match chosen dataset    
import csv
with open(os.path.join(database,dataset,"settings"),"r") as f:
    reader = csv.reader(f)
    settings = [row for row in reader]
try:
    assert opts.COLLIDER == settings[0][1]
except:
    print "Wrong collider settings for this dataset"
    exit(1)
try:
    assert opts.PROCESS == settings[0][2]
except:
    print "Wrong process chosen for this dataset"
    exit(1)   
    
## process to fit
proc = opts.PROCESS
procz = proc+".tgz"

## print out info to screen
print "\nInitialising a topfitter directory named %s\nProcess %s with %s collider settings\nInput data from %s" % (OUTDIR, proc, opts.COLLIDER, dataset )

## copy MadGraph directory
samples=os.path.join(OUTDIR,"samples")
import tarfile
tar = tarfile.open(os.path.join("processes",procz))
tar.extractall()
shutil.move(proc,samples)

## collider type
runcard=os.path.join(OUTDIR,"samples","Cards","run_card.dat")
colcard=os.path.join("colliders",opts.COLLIDER)
shutil.copy(colcard,runcard)

## parameter card from UFO+MG
modcard=os.path.join("models",opts.MODEL)
shutil.copy(modcard,os.path.join(OUTDIR,"param_card_sm.dat"))
  
## copy necessary scripts over    
scripts = ['generate_space.py','run_scan.py','nlo_reweight.py','rebin.py']
for s in scripts:
    shutil.copy(os.path.join("scripts",s),OUTDIR)

## kfactors
kfacdir=os.path.join(OUTDIR,"kfactors")
os.mkdir(kfacdir)
kfacfiles=glob.glob(os.path.join("kfactors",opts.COLLIDER,opts.PROCESS,"*.dat"))
if not kfacfiles:
    print "\nWARNING: K-factors not found for this collider/process combination\n"
for f in kfacfiles:
    shutil.copy(f,kfacdir)

## FastPartons
Analysis="Analysis"
if not opts.XSEC:
    shutil.copytree(Analysis,os.path.join(samples,Analysis))

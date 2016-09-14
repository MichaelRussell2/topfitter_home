#! /usr/bin/env python

"""\
%prog [ipol_order] [ncoeff]
Calculate minimum number of points needed for a given ipol order
"""
import math, sys
import optparse
op = optparse.OptionParser(usage=__doc__)
opts, args = op.parse_args()

import numpy as np

if len(args)!=2:
    print "Enter interpolation order and number of coefficients"
    sys.exit(1)

n, P = int(args[0]), int(args[1])

if n>6:
    print "Don't have that high a polynomial order available"
    sys.exit(1)
        
def Prod(i,P):
    a=[]
    for j in xrange(i):
        a.append(P+j)
    return np.prod(a)/math.factorial(i)

def N(n,P):
    a=[]
    for i in xrange(1,n+1):
        a.append(Prod(i,P))
    return 1+np.sum(a)

print "Order %d polynomial in %d dimensions: require a minimum of %d points" % (n, P, N(n,P)) 

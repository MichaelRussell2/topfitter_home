#! /usr/bin/env python

"""\
Calculate minimum number of points needed for a given ipol order
"""
import math, operator
from functools import reduce
import optparse
op = optparse.OptionParser()
op.add_option("--n","--N", dest="N", type=int, default=2, help="Interpolation order (default: %default)")
op.add_option("--p","--P", dest="P", type=int, default=6, help="Number of coefficients to fit (default=6)")
opts, args = op.parse_args()

import numpy as np

n=opts.N
P=opts.P

if n>6:
    print "Don't have that high a polynomial order available"
    exit(1)
        
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

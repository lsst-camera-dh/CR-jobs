# bias.py
# Acquire bias frames
import sys
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '': 
    count = 1
else:
    count = int(sys.argv[1])

if len(sys.argv) < 3 or sys.argv[2] == '': 
    fbase = "bias"
else:
    fbase = str(sys.argv[2])

if verbose: print 'Acquiring ',count,' bias frames'

if count > 0 and count < 1000:
    for i in range(count):
        if count == 1 :
            if verbose: print 'Acquiring a single bias frame'
            files = acquireBias(fbase)
            if verbose: print files 
        else:
            if verbose: print 'Acquiring exposure frame #',i
            files = acquireBias(fbase+"_%03d" % i)
            if verbose: print files
else:
    print 'Frame count out of range (0..1000)'

# End

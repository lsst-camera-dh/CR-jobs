# dark.py
# Acquire dark frames
import sys
import time
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '':
    dtime = 60.0
else:
    dtime = float(sys.argv[1])

if len(sys.argv) < 3 or sys.argv[2] == '':
    count = 1
else:
    count = int(sys.argv[2])

if len(sys.argv) < 4 or sys.argv[3] == '':
    fbase = "dark"
else:
    fbase = str(sys.argv[3])

if verbose: print 'Acquiring ',count,'  ',dtime,' second dark frames'

if dtime > 0 and dtime < 1000:
    if count > 0 and count < 1000:
        for i in range(count):
            if count == 1 :
                if verbose: print 'Acquiring a single dark frame'
                files = acquireBias(fbase+"_bias")
                files = acquireDark(dtime, fbase+"_dark_%05.2f" % dtime)
                if verbose: print files
            else:
                if verbose: print 'Acquiring dark frame #',i
                files = acquireBias(fbase+"_bias")
                files = acquireDark(dtime, fbase+"_dark_%05.2f_%03d" % (dtime, i))
                if verbose: print files
    else:
        print 'Frame count out of range (0..1000)'
else:
   print 'Integration time out of range (0..1000)'

# End

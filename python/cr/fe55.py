# fe55.py
# Acquire fe55 exposure frames
import sys
import time
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '': 
    exptime = 10.0
else:
    exptime = float(sys.argv[1])

if len(sys.argv) < 3 or sys.argv[2] == '': 
    count = 1
else:
    count = int(sys.argv[2])

if verbose: print 'Acquiring ',count,'  ',exptime,' second fe55 exposure frames'

if exptime > 0 and exptime < 1000:
    if count > 0 and count < 1000:
        for i in range(count):
            if count == 1 :
                #print 'Acquiring a single exposure frame'
                files = acquireBias("fe55_bias")
                if verbose: print files
                #files = acquireDark(exptime, "fe55_dark_%05.2f" % exptime)
                files = acquireExposure(exptime, "fe55_fe55_%05.2f" % exptime)
                if verbose: print files
            else:
                #print 'Acquiring exposure frame #',i
                files = acquireBias("fe55_bias")
                if verbose: print files
                #files = acquireDark(exptime, "fe55_dark_%05.2f_%03d" % (exptime, i))
                files = acquireExposure(exptime, "fe55_fe55_%05.2f_%03d" % (exptime, i))
                if verbose: print files
    else:
        print 'Frame count out of range (0..1000)'
else:
   print 'Exposure time out of range (0..1000)'

# End

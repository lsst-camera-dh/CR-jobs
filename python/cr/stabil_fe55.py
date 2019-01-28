# stabil_fe55.py
# Acquire repeated bias, dark, and fe55 frames for gain stability measurement

# usgae: stabil_fe55.py exptime count delay

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

if len(sys.argv) < 4 or sys.argv[3] == '': 
    delay = 0
else:
    delay = int(sys.argv[3])

if verbose: print 'Acquiring ',count,'  ',exptime,' second fe55 exposure frames with ',delay,' second delay'

if exptime > 0 and exptime < 1000:
    if count > 0 and count < 1000:
        for i in range(count):
            if count == 1 :
                acquireBias("fe55_bias")
                acquireDark(exptime, "fe55_dark_%05.2f" % exptime)
                acquireExposure(exptime, "fe55_fe55_%05.2f" % exptime)
            else:
                acquireBias("fe55_bias_%03d" % i)
                acquireDark(exptime, "fe55_dark_%05.2f_%03d" % (exptime, i))
                acquireExposure(exptime, "fe55_fe55_%05.2f_%03d" % (exptime, i))
                time.sleep(delay)
    else:
        print 'Frame count out of range (0..1000)'
else:
   print 'Exposure time out of range (0..1000)'

# End

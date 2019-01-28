# sbias.py
# Acquire super bias frames
import sys
import time
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '': 
    count = 10
else:
    count = int(sys.argv[1])

if verbose: print 'Acquiring ',count,' bias frames'

if count > 0 and count < 1000:
    for i in range(count):
        print 'Acquiring bias frame #',i
        files = acquireBias("sbias_%03d" % i)
        if verbose: print files
else:
    print 'Frame count out of range (0..1000)'

# End

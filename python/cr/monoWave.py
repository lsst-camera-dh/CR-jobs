# setWl.py
# set the monochromator wavelength
import sys
import time
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) != 2:
    print "Usage: monoWave.py wavelength"
else:
    if sys.argv[1] == '':
        wl = 0.0 
    else:
        wl = float(sys.argv[1])
    if wl > 300 and  wl < 1200 :
        if verbose: print "Setting monochromator wavelength to ", wl
        setWavelength(wl)
    else:
        print "Wavelength: ",wl," out of range (300 - 1200)"

# End

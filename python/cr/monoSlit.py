# setWl.py
# set the monochromator wavelength
import sys
import time
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) != 2:
    print "Usage: monoSlit.py width"
else:
    if sys.argv[1] == '':
        width =  400
    else:
        width = int(sys.argv[1])
    if width > 50 and  width < 2000 :
        if verbose: print "Setting monochromator slit width to ", width
        setSlitWidth(width)
    else:
        print "Wavelength: ",width," out of range (50 - 2000)"

# End

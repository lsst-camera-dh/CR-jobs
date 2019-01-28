# heaterOff.py
from org.lsst.ccs.scripting import *
from REBPSlib import *

verbose = 1

if verbose: print "Turning heater off...."
heaterOff('w')
if verbose: print "Done."

# end

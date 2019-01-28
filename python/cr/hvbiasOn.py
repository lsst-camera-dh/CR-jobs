# bssOn.py
# Turn on the BSS voltage
import sys
from org.lsst.ccs.scripting import *
from REBPSlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '':
    print "Usage: hvbiasOn.py reb"
    print "reb = 'wreb','greb','w','g', or 'both' "
else:
    reb = sys.argv[1]
    if reb in ['wreb','w','greb','g','both']:
        if verbose: print "Turning Back Bias on for ", reb
        if reb in ['wreb','w','both']:
            print 'Turning BSS on for wreb'
            hvbiasOn('w')
        if reb in ['greb','g','both']:
            print 'Turning BSS on for greb'
            hvbiasOn('g')
        if verbose: print "Done."
    else:
        print "Invalid REB name: ",reb

# end

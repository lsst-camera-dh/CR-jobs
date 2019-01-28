# bssOff.py
# Turn off the BSS voltage
import sys
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '':
    print "Usage: bssOff.py reb"
    print "reb = 'wreb','greb','w','g', or 'both' "
else:
    reb = sys.argv[1]
    if reb in ['wreb','w','greb','g','both']:
        if verbose: print "Turning Back Bias off for ", reb
        if reb in ['wreb','w','both']:
            print 'Turning BSS off for wreb'
            setBackBiasOff('w')
        if reb in ['greb','g','both']:
            print 'Turning BSS off for greb'
            setBackBiasOff('g')
        if verbose: print "Done."
    else:
        print "Invalid REB name: ",reb

# end

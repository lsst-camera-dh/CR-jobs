# setBss.py
# Set the HV Bias voltage on the REB Power Supply
import sys
from org.lsst.ccs.scripting import *
from REBlib import *
from REBPSlib import *

verbose = 1

if len(sys.argv) < 3 or sys.argv[1] == '':
    print "Usage: setBss.py reb volts"
    print "reb = 'wreb','greb','w','g', or 'both' "
else:
    reb = sys.argv[1]
    volts = float(sys.argv[2])
    if reb in ['wreb','w','greb','g','both']:
        if verbose: print "Setting Back Bias voltage for ", reb
        if reb in ['wreb','w','both']:
            print 'setting HV Bias voltage for wreb'
            vsetHVBias('w', volts)
        if reb in ['greb','g','both']:
            print 'setting HV Bias voltage for greb'
            vsetHVBias('g', volts)
        if verbose: print "Done."
    else:
        print "Invalid REB name: ",reb

# end

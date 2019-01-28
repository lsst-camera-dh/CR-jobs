# wfsOn.py
# Initialize the WFS voltages
from org.lsst.ccs.scripting import *
from REBlib import *

print "Make sure Back Bias is off..."
setBackBiasOff('w')
print 'WREB Back bias: ',getBackBiasState('w')
ccdPowerUp('w','ITL')



# ccdPowerOn.py
# Initialize the CRTM
from org.lsst.ccs.scripting import *
from REBlib import *

# set the default CCD clock volatges
print "Make sure Back Bias is off..."
setBackBiasOff('w')
print 'WREB Back bias: ',getBackBiasState('w')
setBackBiasOff('g')
print 'GREB Back bias: ',getBackBiasState('g')
ccdPowerUp('w','ITL')
ccdPowerUp('g0','itl')
ccdPowerUp('g1','itl')
#print "turn Back Bias on..."
#setBackBiasOn('w')
#print 'WREB Back bias: ',getBackBiasState('w')
#setBackBiasOn('g')
#print 'GREB Back bias: ',getBackBiasState('g')



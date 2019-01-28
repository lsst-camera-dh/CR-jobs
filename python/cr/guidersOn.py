# guidersOn.py
# Initialize the Guide CCD voltages
from org.lsst.ccs.scripting import *
from REBlib import *

guiderType = 'itl'

print "Turning back bias is off..."
setBackBiasOff('g')
print 'GREB back bias: ', getBackBiasState('g')
ccdPowerUp('g0', guiderType)
ccdPowerUp('g1', guiderType)
print "Turning back bias on..."
setBackBiasOn('g')
print 'GREB back bias: ', getBackBiasState('g')



# ccdPowerOff.py
from org.lsst.ccs.scripting import *
from REBlib import *

print "Make sure Back Bias is off..."
setBackBiasOff('w')
print 'WREB Back bias: ',getBackBiasState('w')
setBackBiasOff('g')
print 'GREB Back bias: ',getBackBiasState('g')

print 'Powering down the WFS CCDs'
ccdPowerDown('w','ITL')

print 'Powering down Guider 0'
ccdPowerDown('g0','e2v')

print 'Powering down Guider 1'
ccdPowerDown('g1','e2v')

print 'CCDs powered down.'



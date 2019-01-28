# guidersOff.py   turn off the guide sensor CCDs
from org.lsst.ccs.scripting import *
from REBlib import *

ccdtype = 'itl'

print "Make sure Back Bias is off..."
setBackBiasOff('g')
print 'GREB Back bias: ',getBackBiasState('g')

print 'Powering down Guider 0'
ccdPowerDown('g0',ccdtype)

print 'Powering down Guider 1'
ccdPowerDown('g1',ccdtype)

print 'Guider CCDs powered down.'



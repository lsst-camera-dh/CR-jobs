# ccdPowerOff.py
from org.lsst.ccs.scripting import *
from REBlib import *

print "Make sure Back Bias is off..."
setBackBiasOff('w')
print 'WREB Back bias: ',getBackBiasState('w')

print 'Powering down the WFS CCDs'
ccdPowerDown('w','ITL')

print 'WFS CCDs powered down.'



# zeroVolts.py
# zero all the voltages without loading DACs until end
import sys
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

zeroVolts('wreb') 
zeroVolts('greb0') 
zeroVolts('greb1') 

#loadDACS('wreb')
#loadDACS('greb0')
#loadDACS('greb1')

# end

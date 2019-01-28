import time
from org.lsst.ccs.scripting import *
from REBPSlib import *

CCS.setThrowExceptions(True)

verbose = 1

ts8 = "ts8-bench"
mono = "ts8-bench/Monochromator"

# ------ Function Definitions -------- #

def getSubsystem():
    subsys = CCS.attachSubsystem(subsystem)
    return subsys

def setWavelength(wl):
    print "Setting wavelength to ",wl
    ts8sub = CCS.attachSubsystem(mono)
    ts8sub.synchCommandLine(1000,"setWaveAndFilter %f " % float(wl))
    time.sleep(30) 



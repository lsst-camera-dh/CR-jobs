import time
from org.lsst.ccs.scripting import *

CCS.setThrowExceptions(True)

verbose = 1

#prefix = "crtm"
#dataDir = "/home/herrmann"

ts7sys = "ts7-2cr"
cryo = ts7sys+'/Cryo'
pdu20 = ts7sys+'/PDU20'
pdu15 = ts7sys+'/PDU15'
vqm = ts7sys+'/VQMonitor'
trubo = ts7sys+'/Turbo'

# ------ Function Definitions -------- #

def getSubsystem():
    subsys = CCS.attachSubsystem(ts7sys)
    return subsys

#def NF55on():
#
#def NF55off():
#
#def PT30on():
#
#def PT30off():
#
#def XEDon():
#
#def XEDoff():
#
#def tempSetPoint(loop,degC):
#
#def tempRamp():

def ts7FilamentOn():
    sub = CCS.attachSubsystem(vqm)
    result = sub.synchCommandLine(1000,"setFilamentOn")

def ts7FilamentOff():
    sub = CCS.attachSubsystem(vqm)
    result = sub.synchCommandLine(1000,"setFilamentOff")

def initCcryo():
    sub = CCS.attachSubsystem(cryo)
    result = sub.synchCommandLine(1000,"setMaxSetPoint 1 30")
    result = sub.synchCommandLine(1000,"setMaxSetPoint 2 30")
    result = sub.synchCommandLine(1000,"setSetPoint 1 -40")
    result = sub.synchCommandLine(1000,"setSetPoint 2 -130")

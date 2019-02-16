import time
from org.lsst.ccs.scripting import *

CCS.setThrowExceptions(True)

verbose = 1

powersupply = "cr-rebps"
wrebps = powersupply+"/WREB"
grebps = powersupply+"/GREB"

# ------ Function Definitions -------- #

def getPowerSubsystem():
    subsys = CCS.attachSubsystem(powersupply)
    return subsys

def getHVBiasVolts(reb):
    if reb in ['w','wreb']:
        rebn = 1
        biasName = '/WREB.hvbias.VbefSwch'
    elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
        rebn = 0
        biasName = '/GREB.hvbias.VbefSwch'
    else:
        print 'REB type ',reb,' not recognized'
        return 
    supply = getPowerSubsystem()
    result = supply.synchCommandLine(1000,biasName+' getValue')
    volts = 0 - float(result.getResult())
    return volts

def setHVBiasDac(reb, val):
    if verbose: print "Setting ", reb, " BSS DAC ", val
    if val >= 0 and val <= 4095:
        if reb in ['w','wreb']:
            rebn = 1
        elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
            rebn = 0
        else:
            print 'REB type ',reb,' not recognized'
            return 
        supply = getPowerSubsystem()
        supply.synchCommandLine(1000,"setBiasDac %d %d" % (rebn,val))
    else:
        print "BSS DAC value of ",val," is out of range (0..4095)"

#def getHVBias(reb):
#        supply = getPowerSubsystem()
#        if reb in ['w','wreb']:
#            supply.synchCommandLine(1000,"" % ())
#            rebn = 'WREB'
#            dacval = volts * -19.40 + 1355.4
#        elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
#            rebn = 0
#            dacval = volts * -37.53 + 1398.9        
#        else:
#            print 'REB type ',reb,' not recognized'
#            return 
#        supply = getPowerSubsystem()
#        supply.synchCommandLine(1000,"setBiasDac %d %d" % (rebn,val))

#def rampHVBiasUp(reb,volts):
#    vsetHVBias(reb,0.0)
#    for i in range(10):
#        vsetHVBias(reb,volts*(i/10.0))
        
#def rampHVBiasUp(reb,volts):
#    vsetHVBias(reb,0.0)
#    for i in range(10):
#        vsetHVBias(reb,volts*(i/10.0))

#def vgetDphi(reb, volts):
#    # for now, swap 'w' and 'g' requests
#    if reb in ['w','wreb']: reb = 'g'
#    elif reb in ['g','greb0','greb1','g1','g0','greb']: reb = 'w'
#    else: reb = reb
#    if verbose: print "Setting ", reb, " Parallel Dphi: ", volts
#    if reb in ['w','wreb']:
#        rebn = 1
#    elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
#        rebn = 0
#    else:
#        print 'REB type ',reb,' not recognized'
#        return 
#    supply = getPowerSubsystem()
#    supply.synchCommandLine(1000,"setDphiDac %d %d" % (rebn,dacval))

        
def vsetHVBias(reb, volts):
    if verbose: print "Setting ", reb, " BSS: ", volts
    if volts >= -70 and volts <= 0:
        if reb in ['w','wreb']:
            rebn = 1
            dacval = volts * -19.40 + 1355.4
        elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
            rebn = 0
            dacval = volts * -37.53 + 1398.9        
        else:
            print 'REB type ',reb,' not recognized'
            return 
        print("HV bias setting disabled out of precaution during testing phase.!!!")
#        setHVBiasDac(reb, dacval)
    else:
        print "BSS voltage of ",volts," is out of range (0..-70)"

def vrampHVBias(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " HV Bias: ", start, stop, step
    volts = start
    if stop > start :
        while volts < stop:
            vsetHVBias(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetHVBias(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetHVBias(reb, stop)

def rampDownHVBias(reb, stop, step):
    hv = getHVBiasVolts(reb)
    vrampHVBias(reb, hv, 0, 5)

def vsetDphi(reb, volts):
    # for now, swap 'w' and 'g' requests
    if reb in ['w','wreb']: reb = 'g'
    elif reb in ['g','greb0','greb1','g1','g0','greb']: reb = 'w'
    else: reb = reb
    if verbose: print "Setting ", reb, " Parallel Dphi: ", volts
    if volts >= 7 and volts <= 12.0:
        if reb in ['w','wreb']:
            rebn = 1
        elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
            rebn = 0
        else:
            print 'REB type ',reb,' not recognized'
            return 
        dacval = abs(12-volts)/5.0 * 4095
        supply = getPowerSubsystem()
        supply.synchCommandLine(1000,"setDphiDac %d %d" % (rebn,dacval))
    else:
        print "Dphi voltage of ",volts," is out of range (7..12)"

def vrampDphi(reb, start,stop,step):
    if verbose: print "Ramping ", reb, " Dphi: ", start, stop, step
    volts = start
    if stop > start :
        while volts < stop:
            vsetDphi(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetDphi(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetDphi(reb, stop)

def voltageState(reb,voltage,state):
    if reb in ['w','wreb']: reb = 'g'
    elif reb in ['g','greb0','greb1','g1','g0','greb']: reb = 'w'
    else: reb = reb
    if verbose: print "Setting ", reb, voltage, state
    if reb in ['w','wreb']:
        rebn = 1
    elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
        rebn = 0
    else:
        print 'REB type ',reb,' not recognized'
        return 
    if verbose: print "Setting ", rebn, voltage, state
    print "setNamedPowerOn %d %s %s" % (rebn,voltage,state)
    supply = getPowerSubsystem()
    supply.synchCommandLine(1000,"setNamedPowerOn %d %s %s" % (rebn,voltage,state))
    

def dphiOn(reb):
    voltageState(reb,'dphi','TRUE')

def dphiOff(reb):
    voltageState(reb,'dphi','FALSE')

def hvbiasOn(reb):
    voltageState(reb,'hvbias','TRUE')

def hvbiasOff(reb):
    voltageState(reb,'hvbias','FALSE')

def powerOn(reb):
    voltageState(reb,'master','TRUE')

def powerOff(reb):
    voltageState(reb,'master','FALSE')

def heaterOn(reb):
    voltageState(reb,'heater','TRUE')

def heaterOff(reb):
    voltageState(reb,'heater','FALSE')

 



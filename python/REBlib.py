import time
from org.lsst.ccs.scripting import *
from REBPSlib import *
from java.time import Duration

CCS.setThrowExceptions(True)

verbose = 1
run = '_9998'  # if not empty string, should start with _
prefix = ''    # if not empty string, should end with _
#dataDir_ = "/home/pdoherty/data"
dataDir_ = '/gpfs/slac/lsst/fs1/g/data/R_and_D/CRTM-001/20190215/'
#dataDir_ = "/home/ccs/crtstdat"

ts8 = "ts8-bench"
mono = "ts8-bench/Monochromator"

subsystem = "cr-raft"                 # 'cr-raft' for use with CR in IR2
greb     = subsystem + "/GREB"        # 
g0biases = subsystem + "/GREB.Bias0"  # 
g1biases = subsystem + "/GREB.Bias1"  #
grails   = subsystem + "/GREB.DAC"    # 
wreb     = subsystem + "/WREB"        # 
wbiases  = subsystem + "/WREB.Bias0"  # 
wrails   = subsystem + "/WREB.DAC"    # 
 
# scaling parameters for the clock voltages
pHi_gain = 0.96
pHi_offset = 0.00
pLo_gain = 0.96
pLo_offset = 0.00
sHi_gain = 0.96
sHi_offset = 0.00
sLo_gain = 0.96
sLo_offset = 0.00
rgHi_gain = 0.96
rgHi_offset = 0.00
rgLo_gain = 0.96
rgLo_offset = 0.00

wOD_gain = 1.00
wOD_offset = 0.00
wRD_gain = 1.00
wRD_offset = 0.00
wOG_gain = 1.00
wOG_offset = 0.00
wGD_gain = 1.00
wGD_offset = 0.00

g0OD_gain = 1.00
g0OD_offset = 0.00
g0RD_gain = 1.00
g0RD_offset = 0.00
g0OG_gain = 1.00
g0OG_offset = 0.00
g0GD_gain = 1.00
g0GD_offset = 0.00

g1OD_gain = 1.00 
g1OD_offset = 0.00
g1RD_gain = 1.00
g1RD_offset = 0.00
g1OG_gain = 1.00
g1OG_offset = 0.00
g1GD_gain = 1.00
g1GD_offset = 0.00

# ------ Function Definitions -------- #

def getSubsystem():
    subsys = CCS.attachSubsystem(subsystem)
    return subsys

def getRaftSubsystem(reb):
    if reb in ['wreb','w']:
        raftsub = CCS.attachSubsystem(wreb)
    elif reb in ['greb','greb0','greb1','g0','g1','g']:
        raftsub = CCS.attachSubsystem(greb)
    else:
        print 'REB type ',reb,' not recognized'
        reftsub = 0
    return raftsub
    
def getRaftBiases(reb):
    if reb in ['wreb','w']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(wreb)
        biases = CCS.attachSubsystem(wbiases)
    elif reb in ['greb','greb0','g0','g']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        biases = CCS.attachSubsystem(g0biases)
    elif reb in ['greb1','g1']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        biases = CCS.attachSubsystem(g1biases)
    else:
        print 'REB type ',reb,' not recognized'
        biases = 0
    return biases
    
def getRaftRails(reb):
    if reb in ['wreb','w']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(wreb)
        rails = CCS.attachSubsystem(wrails)
    elif reb in ['greb','greb0','g0','g']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        rails = CCS.attachSubsystem(grails)
    elif reb in ['greb1','g1']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        rails = CCS.attachSubsystem(grails)
    else:
        print 'REB type ',reb,' not recognized'
        rails = 0
    return rails
        
def getDataDir():
    return dataDir_
    
def setDataDir(cwd):
    global dataDir_
    dataDir_ = cwd
    
def getPrefix():
    return prefix

def setCCD(CCDtype):
    raftsub = CCS.attachSubsystem(subsystem)
    if CCDtype in ['itl','ITL']:
        ccd = 'itl'
    elif CCDtype in ['e2v', 'E2V']:
        ccd = 'e2v'
    else:
        print 'CCD type ', CCDtype, ' not recognized'
        return    
    print 'CCD = %s' % ccd
    result = raftsub.sendSynchCommand("change ccdType %s" % ccd)    
    print result

def getCCD():
    raftsub = CCS.attachSubsystem(subsystem)
    ccdType = raftsub.sendSynchCommand("getCcdType") 
    print "CCD Type = ",ccdType
    return ccdType
    
def setFilebase(filebase):
    raftsub = CCS.attachSubsystem(subsystem)
#    fname = filebase + "_${timestamp}.fits"
    fname = filebase
    raftsub.sendSynchCommand("setFitsFileNamePattern " + fname)

def setFilename(filebase):
    raftsub = CCS.attachSubsystem(subsystem)
#    fname = prefix + "${rebName}${sensorId}_" + filebase + run + "_${timestamp}.fits" #for GREB
    fname = filebase
    # for a single sensor from one REB: fname = prefix + filebase + "_${timestamp}.fits" #for WREB
    print "Filename : ",fname
    raftsub.sendSynchCommand("setFitsFileNamePattern " + fname)
#    raftsub.sendSynchCommand("setFitsFileNamePattern blah.fits")

#def crtmInit():
    # configure the sequencer
    #wreb_seqfile = '/lsst/ccs/sequences/seq-e2v-2s.seq'
    #greb_seqfile = '/lsst/ccs/sequences/seq-e2v-2s.seq'
    #print 'Loading WREB sequencer file ',wreb_seqfile
    #loadSeq('w',wreb_seqfile)
    #print 'Loading GREB sequencer file ',greb_seqfile
    #loadSeq('g',greb_seqfile)
    # set the default CCD clock volatges
#    print "Make sure Back Bias is off..."
#    setBackBiasOff('w')
#    setBackBiasOff('g')
#    time.sleep(3)
#    ccdPowerUp('w','ITL')
#    ccdPowerUp('g0','e2v')
#    ccdPowerUp('g1','e2v')
#    time.sleep(1)
#    print "turn Back Bias on..."
#    setBackBiasOn('w')
#    setBackBiasOn('g')

def aspicGain(reb, value):
    if verbose: print "Setting ASPIC gain on " + reb
    board = getRaftSubsystem(reb)
    board.sendSynchCommand("setAllAspicGain %d" % value)    
    board.sendSynchCommand("loadAspics true")   
    time.sleep(0.1)

def aspicRC(reb, value):
    if verbose: print "Setting ASPIC RC on " + reb
    board = getRaftSubsystem(reb)
    board.sendSynchCommand("setAllAspicRc %d" % value)    
    board.sendSynchCommand("loadAspics true")   
    time.sleep(0.1)

def loadAspics(reb):
    if verbose: print "Loading ASPICs on " + reb
    board = getRaftSubsystem(reb)
    board.sendSynchCommand("loadAspics true")   
    
def loadDACS(reb):
    #if verbose: print "Loading DACs on " + reb
    board = getRaftSubsystem(reb)
    board.sendSynchCommand("loadDacs true")    
    board.sendSynchCommand("loadBiasDacs true")    
    # result = board.sendSynchCommand("loadAspics true")   
    #time.sleep(1)

def zeroVolts(reb):  # zeros values in memory, does not load DACs
    biases = getRaftBiases(reb)
    biases.sendSynchCommand("change odP 0.01" )
    biases.sendSynchCommand("change rdP 0" )
    biases.sendSynchCommand("change gdP 0" )
    biases.sendSynchCommand("change ogP 0" )
    rails = getRaftRails(reb)
    rails.sendSynchCommand("change pclkLowP 0")
    rails.sendSynchCommand("change pclkHighP 0")
    rails.sendSynchCommand("change sclkLowP 0")
    rails.sendSynchCommand("change sclkHighP 0")
    rails.sendSynchCommand("change rgLowP 0")
    rails.sendSynchCommand("change rgHighP 0")

def vsetOD(reb, volts):
    if verbose: print "Setting ", reb, " OD: ", volts
    biases = getRaftBiases(reb)
    if reb in ['wreb','w']:
        volts = volts * wOD_gain + wOD_offset
    elif reb in ['greb','greb0','g0','g']:
        volts = volts * g0OD_gain + g0OD_offset
    elif reb in ['greb1','g1']:
        volts = volts * g1OD_gain + g1OD_offset
    else:
        print 'REB type ',reb,' not recognized'
    biases.sendSynchCommand("change odP %f" % volts)
    loadDACS(reb)   

def vrampOD(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " OD: ", start, stop, step
    volts = start 
    if stop > start:
        while volts < stop:
            vsetOD(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start:
        while volts > stop:
            vsetOD(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetOD(reb, stop)

def vsetRD(reb, volts):
    if verbose: print "Setting ", reb, " RD: ", volts
    biases = getRaftBiases(reb)
    if reb in ['wreb','w']:
        volts = volts * wRD_gain + wRD_offset
    elif reb in ['greb','greb0','g0','g']:
        volts = volts * g0RD_gain + g0RD_offset
    elif reb in ['greb1','g1']:
        volts = volts * g1RD_gain + g1RD_offset
    else:
        print 'REB type ',reb,' not recognized'
    biases.sendSynchCommand("change rdP %f" % volts)
    loadDACS(reb)   

def vrampRD(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " RD: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetRD(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetRD(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetRD(reb, stop)

def vsetOG(reb, volts):
    if verbose: print "Setting ", reb, " OG: ", volts
    biases = getRaftBiases(reb)
    if reb in ['wreb','w']:
        volts = volts * wOG_gain + wOG_offset
    elif reb in ['greb','greb0','g0','g']:
        volts = volts * g0OG_gain + g0OG_offset
    elif reb in ['greb1','g1']:
        volts = volts * g1OG_gain + g1OG_offset
    else:
        print 'REB type ',reb,' not recognized'
    biases.sendSynchCommand("change ogP %f" % volts)
    loadDACS(reb)   

def vrampOG(reb, start,stop,step):
    if verbose: print "Ramping ", reb, " OG: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetOG(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetOG(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetOG(reb, stop)

def vsetGD(reb, volts):
    if verbose: print "Setting ", reb, " GD: ", volts
    biases = getRaftBiases(reb)
    if reb in ['wreb','w']:
        volts = volts * wGD_gain + wGD_offset
    elif reb in ['greb','greb0','g0','g']:
        volts = volts * g0GD_gain + g0GD_offset
    elif reb in ['greb1','g1']:
        volts = volts * g1GD_gain + g1GD_offset
    else:
        print 'REB type ',reb,' not recognized'
    biases.sendSynchCommand("change gdP %f" % volts)
    loadDACS(reb)   

def vrampGD(reb, start,stop,step):
    if verbose: print "Ramping ", reb, " GD: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetGD(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetGD(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetGD(reb, stop)

def vsetParLo(reb, volts):
    if verbose: print "Setting ", reb, " Parallel low: ", volts
    rails = getRaftRails(reb)
    volts = volts * pLo_gain + pLo_offset
    rails.sendSynchCommand("change pclkLowP %f" % volts)
    loadDACS(reb)

def vrampParLo(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " Parallel Low: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetParLo(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetParLo(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetParLo(reb, stop)
 
def vsetParHi(reb, volts):
    if verbose: print "Setting ", reb, " Parallel high: ", volts
    rails = getRaftRails(reb)
    volts = volts * pHi_gain + pHi_offset
    rails.sendSynchCommand("change pclkHighP %f" % volts)
    loadDACS(reb)

def vrampParHi(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " Parallel High: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetParHi(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetParHi(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetParHi(reb, stop)

def vsetSerLo(reb, volts):
    if verbose: print "Setting ", reb, " Serial low: ", volts
    rails = getRaftRails(reb)
    volts = volts * sLo_gain + sLo_offset
    rails.sendSynchCommand("change sclkLowP %f" % volts)
    loadDACS(reb)

def vrampSerLo(reb, start,stop,step):
    if verbose: print "Ramping ", reb, " Serial Low: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetSerLo(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetSerLo(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetSerLo(reb, stop)
 
def vsetSerHi(reb, volts):
    if verbose: print "Setting ", reb, " Serial high: ", volts
    rails = getRaftRails(reb)
    volts = volts * sHi_gain + sHi_offset
    rails.sendSynchCommand("change sclkHighP %f" % volts)
    loadDACS(reb)

def vrampSerHi(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " Serial High: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetSerHi(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetSerHi(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetSerHi(reb, stop)
 
def vsetRGLo(reb, volts):
    if verbose: print "Setting ", reb, " RG low: ", volts
    rails = getRaftRails(reb)
    volts = volts * rgLo_gain + rgLo_offset
    rails.sendSynchCommand("change rgLowP %f" % volts)
    loadDACS(reb)

def vrampRGLo(reb, start, stop, step):
    if verbose: print "Ramping ", reb, " RG Low: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetRGLo(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetRGLo(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetRGLo(reb, stop)

def vsetRGHi(reb, volts):
    if verbose: print "Setting ", reb, " RG high: ", volts
    rails = getRaftRails(reb)
    volts = volts * rgHi_gain + rgHi_offset
    rails.sendSynchCommand("change rgHighP %f" % volts)
    loadDACS(reb)

def vrampRGHi(reb, start,stop,step):
    if verbose: print "Ramping ", reb, " RG high: ", start, stop, step
    volts = start 
    if stop > start :
        while volts < stop:
            vsetRGHi(reb, volts)
            volts = min(volts + abs(step), stop)
    elif stop < start :
        while volts > stop:
            vsetRGHi(reb, volts)
            volts = max(volts - abs(step), stop)
    vsetRGHi(reb, stop)

def ccdPowerUp(reb, ccd):
    if ccd.upper() in ['e2v','E2V']: 
        vsetRD(reb,18.0)
        vsetOD(reb,30.0)
        vsetGD(reb,26.0)
        vsetOG(reb,4.0)
        vsetSerLo(reb,0.50)
        vsetSerHi(reb,+9.5)
        vsetParLo(reb,0.0)
        vsetParHi(reb,+9.0)
        vsetRGLo(reb,0.0)
        vsetRGHi(reb,+11.5)
        vsetDphi(reb,+8.0)
        dphiOn(reb)
    elif ccd.upper() in ['ITL','ITLA','ITL_A']:
        vrampSerLo(reb,0,-5.0, 2.0)
        vrampSerHi(reb,0,+5.0, 2.0)
        vrampParLo(reb,0,-8.0, 2.0)
        vrampParHi(reb,0,+3.0, 1.0)
        dphiOn(reb)
        vrampDphi(reb,7,+10.0, 1.0)
        vrampRGLo(reb,0,-2.0, 1.0)
        vrampRGHi(reb,0,+8.0, 2.0)
        vrampOG(reb,0,-2.0, 1.0)
        vrampGD(reb,0,20.0, 4.0)
        vrampRD(reb,0,13.0, 3.0)
        vrampOD(reb,0,26.0, 4.0)
    elif ccd.upper() in ['ITLB','ITL_B']:
        vsetSerLo(reb,-8.0)
        vsetSerHi(reb,+4.0)
        vsetParLo(reb,-8.0)
        vsetParHi(reb,+3.0)
        vsetRGLo(reb,-2.0)
        vsetRGHi(reb,+8.0)
        vsetOG(reb,+3.0)
        vsetGD(reb,20.0)
        vsetRD(reb,13.0)
        vsetOD(reb,26.0)
        vsetDphi(reb,+10.0)
        dphiOn(reb)
    else:
        print 'CCD type ',ccd,' not recognized'
    print 'Device type: ',ccd,' powered on.'   

def ccdPowerDown(reb, ccd):
    setBackBiasOff(reb)
    if ccd.upper() in ['E2V']: 
        vsetRGHi(reb,0.0)
        vsetRGLo(reb,0.0)
        vsetParHi(reb,0.0)
        vsetDphi(reb,7.0)
        dphiOff(reb)
        vsetParLo(reb,0.0)
        vsetSerHi(reb,0.0)
        vsetSerLo(reb,0.0)
        vsetOG(reb,0.0)
        vsetGD(reb,0.0)
        vsetOD(reb,0.0)
        vsetRD(reb,0.0)
    elif ccd.upper() in ['ITL','ITLA','ITLB','ITL_A','ITL_B']:
        vsetOD(reb,0.0)
        vsetRD(reb,0.0)
        vsetGD(reb,0.0)
        vsetOG(reb,0.0)
        vsetRGHi(reb,0.0)
        vsetRGLo(reb,0.0)
        vsetParHi(reb,0.0)
        vsetDphi(reb,7.0)
        dphiOff(reb)
        vsetParLo(reb,0.0)
        vsetSerHi(reb,0.0)
        vsetSerLo(reb,0.0)
    else:
        print 'CCD type ',ccd,' not recognized'
    print 'Device type: ',ccd,' powered off.'   


def ITLdefaults(reb):
    if verbose: print "Seting default ITL voltages"
    vsetParLo(reb,-8.0)
    vsetParHi(reb,+3.0)
    vsetSerLo(reb,-5.0)
    vsetSerHi(reb,+5.0)
    vsetRGLo(reb,-2.0)
    vsetRGHi(reb,+8.0)
    vsetRD(reb,13.0)
    vsetOG(reb,-2.0)
    vsetOD(reb,26.0)
    vsetGD(reb,20.0)

def setSeqStart(reb,main):
    subsys=getRaftSubsystem(reb)
    subsys.synchCommand(10, "setSequencerStart", main)

def setParameterValue(reb, param, value):
    subsys=getRaftSubsystem(reb)
    subsys.synchCommand(10, "setSequencerParameter", param, value)

def startSeq(reb):
    subsys=getRaftSubsystem(reb)
    result = subsys.synchCommand(10, "startSequencer")
    if verbose: print result

def loadSeq(reb, seqfile):
    if verbose: print 'Loading sequencer file: ',seqfile,' to REB: ',reb
    subsys=getSubsystem()
    result=subsys.synchCommand(20, "loadSequencer", seqfile)
    if verbose: print result

def getSeqParam(name):
    subsys=getSubsystem()
    result=subsys.synchCommand(200, "getSequencerParameter %s", name)
    print result
    return result
    
def getBackBiasState(reb):
    if verbose: print "Getting BackBias status...",
    board = getRaftSubsystem(reb)
    result = board.synchCommand(10, "isBackBiasOn ")
    if verbose: print result
    return result

def setBackBiasOn(reb):
    if verbose: print "setting BackBias On...",
    board = getRaftSubsystem(reb)
    board.synchCommand(10, "setBackBias true")
    time.sleep(3) # allow some settling time
    #if verbose: print 'Done.'
    state = getBackBiasState(reb)
    if verbose: print 'Back Bias State = ',state
    return state

def setBackBiasOff(reb):
    if verbose: print "setting BackBias Off...",
    board = getRaftSubsystem(reb)
    board.synchCommand(10, "setBackBias false")
    time.sleep(3) # allow some settling time
    #if verbose: print 'Done.'
    state = getBackBiasState(reb)
    if verbose: print 'Back Bias State = ',state
    return state

# functions for acquiring image data

def acquire(exptime):
    raftsub = CCS.attachSubsystem(subsystem)
#    raftsub.sendSynchCommand("monitor-update change taskPeriodMillis -1")  # stop monitoring REBs (noisy)

    timeout = int((exptime + 10) * 1000) 

    raftsub.sendSynchCommand(Duration.ofSeconds(timeout/1000),"acquireImage")
#   raftsub.sendSynchCommand("startSequencer")   # not needed with new firmware

    if verbose: print 'acquire: timeout =', timeout 
    raftsub.sendSynchCommand(Duration.ofSeconds(timeout/1000),"waitForImage %i" % int(timeout))
#    raftsub.sendSynchCommand("monitor-update change taskPeriodMillis 1000")  # restart monitorinng REBs
    dataDir_ = getDataDir()
    if verbose: print "Saving FITS image to ", dataDir_
#    raftsub.sendSynchCommand("setFitsFileNamePattern blah.fits")
    result = raftsub.sendSynchCommand(Duration.ofSeconds(120),"saveFitsImage",dataDir_)
    if verbose: print result
    return result

def acquireBias(filebase):
    if verbose: print "Acquire Bias: Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.sendSynchCommand("setSequencerStart Bias")
    #if verbose: print result
    raftsub.sendSynchCommand("setExposureTime 0")
    raftsub.sendSynchCommand("setSequencerParameter ExposureTime 0")
    setFilename(filebase)
    return acquire(0)

def acquireDark(exptime, filebase):
    if verbose: print "Acquire Dark:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
#    result = raftsub.sendSynchCommand("setSequencerStart Dark")
    #if verbose: print result
    raftsub.sendSynchCommand("setExposureTime %i" % long(exptime))
    raftsub.sendSynchCommand("setSequencerParameter ExposureTime %i" % long(exptime * 1000.0 / 25))
    setFilename(filebase)
    return acquire(exptime)

# added to match standard harnessed job scripts for EO acquisitions
def acquireExposureMaster(exptime, dolight, doXED, cwd, filebase):
    setDataDir(cwd)
    print("dataDir_ = ",dataDir_)
    if exptime == 0.0 :
        files = acquireBias(filebase)
    elif not dolight and not doXED :
        files = acquireDark(exptime/1000., filebase)
    elif not dolight and doXED :
        files = null
        print("XED functionality not implimented for Corner Raft")
    else :
        files = acquireExposure(exptime, filebase)
    return files


def acquireExposure(exptime, filebase):
    if verbose: print "Acquire Exposure:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.sendSynchCommand("setSequencerStart Exposure")
    #if verbose: print result
    raftsub.sendSynchCommand("setExposureTime %i" % long(exptime))
    raftsub.sendSynchCommand("setSequencerParameter ExposureTime %i" % long(exptime * 1000 / 25))
#    setFilename(filebase)
    return acquire(exptime)

def acquirePumped(exptime, filebase):
    if verbose: print "Acquire Pumped Exposure:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.sendSynchCommand("setSequencerStart PocketPump")
    #if verbose: print result
    raftsub.sendSynchCommand("setExposureTime %i" % long(exptime))
    raftsub.sendSynchCommand("setSequencerParameter ExposureTime %i" % long(exptime * 1000 / 25))
    setFilename(filebase)
    return acquire(exptime)
   
   
# Stuff that should go into ts8lib.py sometime
def setWavelength(wl):
    print "Setting wavelength to ",wl
    ts8sub = CCS.attachSubsystem(mono)
    ts8sub.sendSynchCommand(Duration.ofSeconds(7),"setWaveAndFilter %f " % float(wl))
#    time.sleep(30) 

def setSlitWidth(width):
    print "Setting slit width to ",width
    ts8sub = CCS.attachSubsystem(mono)
    ts8sub.sendSynchCommand("setSlitSize 1 %d " % int(width))
    ts8sub.sendSynchCommand("setSlitSize 2 %d " % int(width))
    time.sleep(30)




# def clearCCD():
#    print "Clearing CCD "
#    raftsub = CCS.attachSubsystem(subsystem)
#    result = raftsub.sendSynchCommand("setSequencerStart Clear")
#    result = raftsub.sendSynchCommand("startSequencer")

# end function definitions #



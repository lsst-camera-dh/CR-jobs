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

    timeout = int((exptime + 120.0) * 1000.0)


    if verbose: print 'acquire: doing acquireImage' 
    result = raftsub.sendSynchCommand(Duration.ofMillis(timeout),"acquireImage")

    time.sleep(exptime)

    if exptime==0 :
        if verbose: print 'acquire: doing Bias (ReadFrame)' 
        result = raftsub.sendSynchCommand("setSequencerStart Bias")
    else :
        if verbose: print 'acquire: doing Acquire (ReadFrame)' 
        result = raftsub.sendSynchCommand("setSequencerStart Acquire")
    result = raftsub.sendSynchCommand("startSequencer") 


    if verbose: print 'acquire: Waiting for Image ... timeout =', timeout 
    result = raftsub.sendSynchCommand(Duration.ofMillis(timeout),"waitForImage 30000")

    if result == 0 :
        raise Exception,"Timeout waiting for image"

#    raftsub.sendSynchCommand("monitor-update change taskPeriodMillis 1000")  # restart monitorinng REBs

    dataDir_ = getDataDir()
    if verbose: print "Saving FITS image to ", dataDir_
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
    try:
        result = raftsub.sendSynchCommand("setSequencerStart Dark")
    except:
        print("Failed to set sequencer start to Exposure!!! Proceeding during development period")
    #if verbose: print result
    raftsub.sendSynchCommand("setExposureTime %i" % long(exptime))
    raftsub.sendSynchCommand("setSequencerParameter ExposureTime %i" % long(exptime * 1000.0 / 25))
    setFilename(filebase)
    return acquire(exptime)

# added to match standard harnessed job scripts for EO acquisitions
def acquireExposureMaster(exptime, dolight, doXED, cwd, filebase, doppump = False ):
    setDataDir(cwd)
    print("dataDir_ = ",dataDir_)

    raftsub = CCS.attachSubsystem(subsystem)

# ------- pointer adjustment for choosing dark/flat exposure type
    subs = raftsub.sendSynchCommand("getSequencerSubroutineMap")[0]

#    submap = {}
#    for sub in subs.entrySet():
#        print "%s=%d" % (sub.getKey(),sub.getValue())
#        submap[sub.getKey()] = sub.getValue()

#        if "ExposureFlush" in sub.getKey() :
#            ExpFlush = sub.getValue()
#            print "ExpFlush value = ",ExpFlush
#        if "SerialFlush" in sub.getKey() :
#            SerFlush = sub.getValue()
#            print "Serial value = ",SerFlush
#    print "submap=\n",submap

#    pntrs = raftsub.sendSynchCommand("getSequencerPointers")[0]
#    for pntr in pntrs.entrySet():
#        print "%s=%d" % (pntr.getKey(),pntr.getValue().value)

    flushpntr = None
    if dolight or doXED :
        flushpntr = int(subs["ExposureFlush"])
        print "setting exposure to ExposureFlush with index ",flushpntr
    else :
        flushpntr = int(subs["SerialFlush"])
        print "setting exposure to SerialFlush with index ",flushpntr
    pntrs = raftsub.sendSynchCommand("setSequencerParameter %s %s" % ("Exposure",str(flushpntr)))
# -------

    if exptime == 0.0 :
        files = acquireBias(filebase)
    else :
        files = acquireExposure(exptime/1000., filebase, doppump)
#    elif not dolight and not doXED :
#        files = acquireDark(exptime/1000., filebase)
#    elif not dolight and doXED :
#        files = acquireDark(exptime/1000., filebase)
#        print("XED functionality not implimented for Corner Raft")
#    else :
#        files = acquireExposure(exptime/1000., filebase)


# move to top harnessed job level
#    if doXED :
#        pdusub = CCS.attachSubsystem("ts7-2cr/PDU20")
#        pdusub.sendSynchCommand("PDU20 forceOutletOn XED-CONTROL")


    print("list of files produced = ",files)
    return files


def acquireExposure(exptime, filebase, doppump=False):
    if verbose: print "Acquire Exposure:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)

    raftsub.sendSynchCommand("setExposureTime %i" % long(exptime))
    print("setSequencerParameter ExposureTime %i" % long(exptime * 1000 / 25))
    raftsub.sendSynchCommand("setSequencerParameter ExposureTime %i" % long(exptime * 1000 / 25))
#    setFilename(filebase)

    try:
#        result = raftsub.sendSynchCommand("setSequencerStart Exposure")
        print("set sequencer start to Expose")
        if not doppump :
            result = raftsub.sendSynchCommand("setSequencerStart Expose")
        else :
            result = raftsub.sendSynchCommand("setSequencerStart PocketPump")

    except:
        print("Failed to set sequencer start to Exposure!!! Proceeding during development period")

    #if verbose: print result
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



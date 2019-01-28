import time
from org.lsst.ccs.scripting import *

CCS.setThrowExceptions(True)

verbose = 1

prefix = "crtm2"
#dataDir = "/home/pdoherty/data"
dataDir = '/gpfs/slac/lsst/fs1/g/data/R_and_D/CRTM-002/'

ts8 = "ts8-bench"
mono = "ts8-bench/Monochromator"

powersupply = "cr-rebps"
wrebps = powersupply+"/WREB"
grebps = powersupply+"/GREB"

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

def getPowerSubsystem():
    subsys = CCS.attachSubsystem(powersupply)
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
    return dataDir
    
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
    result = raftsub.synchCommandLine(1000,"setCcdType %s" % ccd)    
    print result.getResult()

def getCCD():
    raftsub = CCS.attachSubsystem(subsystem)
    ccdType = raftsub.synchCommandLine(1000,"getCcdType").getResult() 
    print "CCD Type = ",ccdType
    return ccdType
    
def setFilebase(filebase):
    raftsub = CCS.attachSubsystem(subsystem)
    fname = filebase + "_${timestamp}.fits"
    raftsub.synchCommandLine(1000, "setFitsFileNamePattern " + fname)

def setFilename(filebase):
    raftsub = CCS.attachSubsystem(subsystem)
    fname = prefix + "_${rebName}${sensorId}_" + filebase + "_${timestamp}.fits" #for GREB
    # for a single sensor from one REB: fname = prefix + '_' + filebase + "_${timestamp}.fits" #for WREB
    print "Filename : ",fname
    raftsub.synchCommandLine(1000, "setFitsFileNamePattern " + fname)

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
    board.synchCommandLine(1000,"setAllAspicGain %d" % value)    
    board.synchCommandLine(1000,"loadAspics true")   
    time.sleep(0.1)

def aspicRC(reb, value):
    if verbose: print "Setting ASPIC RC on " + reb
    board = getRaftSubsystem(reb)
    board.synchCommandLine(1000,"setAllAspicRc %d" % value)    
    board.synchCommandLine(1000,"loadAspics true")   
    time.sleep(0.1)

def loadAspics(reb):
    if verbose: print "Loading ASPICs on " + reb
    board = getRaftSubsystem(reb)
    board.synchCommandLine(1000,"loadAspics true")   
    
def loadDACS(reb):
    #if verbose: print "Loading DACs on " + reb
    board = getRaftSubsystem(reb)
    board.synchCommandLine(1000,"loadDacs true")    
    board.synchCommandLine(1000,"loadBiasDacs true")    
    # result = board.synchCommandLine(1000,"loadAspics true")   
    time.sleep(1)

def zeroVolts(reb):  # zeros values in memory, does not load DACs
    biases = getRaftBiases(reb)
    biases.synchCommandLine(1000,"change odP 0" )
    biases.synchCommandLine(1000,"change rdP 0" )
    biases.synchCommandLine(1000,"change gdP 0" )
    biases.synchCommandLine(1000,"change ogP 0" )
    rails = getRaftRails(reb)
    rails.synchCommandLine(1000,"change pclkLowP 0")
    rails.synchCommandLine(1000,"change pclkHighP 0")
    rails.synchCommandLine(1000,"change sclkLowP 0")
    rails.synchCommandLine(1000,"change sclkHighP 0")
    rails.synchCommandLine(1000,"change rgLowP 0")
    rails.synchCommandLine(1000,"change rgHighP 0")

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
    biases.synchCommandLine(1000,"change odP %f" % volts)
    loadDACS(reb)   

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
    biases.synchCommandLine(1000,"change rdP %f" % volts)
    loadDACS(reb)   

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
    biases.synchCommandLine(1000,"change ogP %f" % volts)
    loadDACS(reb)   

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
    biases.synchCommandLine(1000,"change gdP %f" % volts)
    loadDACS(reb)   

def getBiasDac(reb):
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
    supply = supply+'/'+biasName
    result =supply.synchCommandLine(1000,"setBiasDac %d %d" % (rebn,val))

def setBiasDac(reb, val):
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

def vsetBias(reb, volts):
    if verbose: print "Setting ", reb, " BSS: ", volts
    if volts >= -70 and volts <= 0:
        if reb in ['w','wreb']:
            rebn = 1
        elif reb in ['greb','greb0','g0','g', 'greb1','g1']:
            rebn = 0
        else:
            print 'REB type ',reb,' not recognized'
            return 
        dacval = (volts/-70.0) * 4095        
        supply = getPowerSubsystem()
        if verbose: print "Setting BBS on ", reb, " to volts. DAC = ",dacval
        supply.synchCommandLine(1000,"setBiasDac %d %d" % (rebn,dacval))
    else:
        print "BSS voltage of ",volts," is out of range (0..-70)"

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

def vsetParLo(reb, volts):
    if verbose: print "Setting ", reb, " Parallel low: ", volts
    rails = getRaftRails(reb)
    volts = volts * pLo_gain + pLo_offset
    rails.synchCommandLine(1000,"change pclkLowP %f" % volts)
    loadDACS(reb)
 
def vsetParHi(reb, volts):
    if verbose: print "Setting ", reb, " Parallel high: ", volts
    rails = getRaftRails(reb)
    volts = volts * pHi_gain + pHi_offset
    rails.synchCommandLine(1000,"change pclkHighP %f" % volts)
    loadDACS(reb)
 
def vsetSerLo(reb, volts):
    if verbose: print "Setting ", reb, " Serial low: ", volts
    rails = getRaftRails(reb)
    volts = volts * sLo_gain + sLo_offset
    rails.synchCommandLine(1000,"change sclkLowP %f" % volts)
    loadDACS(reb)
 
def vsetSerHi(reb, volts):
    if verbose: print "Setting ", reb, " Serial high: ", volts
    rails = getRaftRails(reb)
    volts = volts * sHi_gain + sHi_offset
    rails.synchCommandLine(1000,"change sclkHighP %f" % volts)
    loadDACS(reb)
 
def vsetRGLo(reb, volts):
    if verbose: print "Setting ", reb, " RG low: ", volts
    rails = getRaftRails(reb)
    volts = volts * rgLo_gain + rgLo_offset
    rails.synchCommandLine(1000,"change rgLowP %f" % volts)
    loadDACS(reb)

def vsetRGHi(reb, volts):
    if verbose: print "Setting ", reb, " RG high: ", volts
    rails = getRaftRails(reb)
    volts = volts * rgHi_gain + rgHi_offset
    rails.synchCommandLine(1000,"change rgHighP %f" % volts)
    loadDACS(reb)

def ccdPowerUp(reb, ccd):
    if ccd in ['e2v','E2V']: 
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
    elif ccd in ['itl','ITL']:
        vsetSerLo(reb,-5.0)
        vsetSerHi(reb,+5.0)
        vsetParLo(reb,-8.0)
        vsetParHi(reb,+3.0)
        vsetRGLo(reb,-2.0)
        vsetRGHi(reb,+8.0)
        vsetOG(reb,-2.0)
        vsetGD(reb,20.0)
        vsetRD(reb,13.0)
        vsetOD(reb,26.0)
        vsetDphi(reb,+10.0)
    else:
        print 'CCD type ',ccd,' not recognized'
    print 'Device type: ',ccd,' powered on.'   

def ccdPowerDown(reb, ccd):
    setBackBiasOff(reb)
    if ccd in ['e2v','E2V']: 
        vsetRGHi(reb,0.0)
        vsetRGLo(reb,0.0)
        vsetParHi(reb,0.0)
        vsetDphi(reb,7.0)
        vsetParLo(reb,0.0)
        vsetSerHi(reb,0.0)
        vsetSerLo(reb,0.0)
        vsetOG(reb,0.0)
        vsetGD(reb,0.0)
        vsetOD(reb,0.0)
        vsetRD(reb,0.0)
    elif ccd in ['itl','ITL']:
        vsetOD(reb,0.0)
        vsetRD(reb,0.0)
        vsetGD(reb,0.0)
        vsetOG(reb,0.0)
        vsetRGHi(reb,0.0)
        vsetRGLo(reb,0.0)
        vsetParHi(reb,0.0)
        vsetDphi(reb,7.0)
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
    if verbose: print result.getResult()

def loadSeq(reb, seqfile):
    subsys=getSubsystem()
    result=subsys.synchCommand(20, "loadSequencer", seqfile)
    if verbose: print result.getResult()

def getSeqParam(name):
    subsys=getSubsystem()
    result=subsys.synchCommand(200, "getSequencerParameter %s", name)
    print result.getResult()
    return result
    
def getBackBiasState(reb):
    if verbose: print "Getting BackBias status...",
    board = getRaftSubsystem(reb)
    result = board.synchCommand(10, "isBackBiasOn ")
    if verbose: print result.getResult()
    return result.getResult()

def setBackBiasOn(reb):
    if verbose: print "setting BackBias On...",
    board = getRaftSubsystem(reb)
    board.synchCommand(10, "setBackBias true")
    time.sleep(3) # allow some settling time
    if verbose: print 'Done.'
    state = getBackBiasState(reb)
    if verbose: print 'Back Bias State = ',state
    return state

def setBackBiasOff(reb):
    if verbose: print "setting BackBias Off...",
    board = getRaftSubsystem(reb)
    board.synchCommand(10, "setBackBias false")
    time.sleep(3) # allow some settling time
    if verbose: print 'Done.'
    state = getBackBiasState(reb)
    if verbose: print 'Back Bias State = ',state
    return state

# functions for acquiring image data

def acquire(exptime):
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"acquireImage")
# No longer needed since WREB firmware update
    result = raftsub.synchCommandLine(1000,"startSequencer")
# Would be better to wait for image, but not available in this version of Rafts subsystem
    #time.sleep(exptime + 10) 
    #raftsub.synchCommandLine(15000,"waitSequencerDone")
    timeout = int((exptime + 10) * 1000) 
    if verbose: print 'acquire: timout =', timeout 
    raftsub.synchCommandLine(1000,"waitForImage %i" % int(timeout))
    if verbose: print "Saving FITS image to ", dataDir
    result = raftsub.synchCommand(1000,"saveFitsImage " + dataDir)
    if verbose: print result.getResult()
    return result.getResult()

def acquireBias(filebase):
    if verbose: print "Acquire Bias: Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart Bias")
    if verbose: print result.getResult()
    raftsub.synchCommandLine(1000,"setSequencerParameter ExposureTime 0")
    setFilename(filebase)
    return acquire(0)

def acquireDark(exptime, filebase):
    if verbose: print "Acquire Dark:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart Dark")
    if verbose: print result.getResult()
    raftsub.synchCommandLine(1000,"setSequencerParameter ExposureTime "+("%i" % long(exptime * 1000.0 / 25)))
    setFilename(filebase)
    return acquire(exptime)

def acquireExposure(exptime, filebase):
    if verbose: print "Acquire Exposure:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart Exposure")
    if verbose: print result.getResult()
    raftsub.synchCommandLine(1000,"setSequencerParameter ExposureTime "+("%i" % long(exptime * 1000.0 / 25)))
    setFilename(filebase)
    return acquire(exptime)

def acquirePumped(exptime, filebase):
    if verbose: print "Acquire Pumped Exposure:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart PocketPump")
    if verbose: print result.getResult()
    raftsub.synchCommandLine(1000,"setSequencerParameter ExposureTime "+("%i" % long(exptime * 1000.0 / 25)))
    setFilename(filebase)
    return acquire(exptime)
   
   
# Stuff that should go into ts8lib.py sometime
def setWavelength(wl):
    print "Setting wavelength to ",wl
    ts8sub = CCS.attachSubsystem(mono)
    ts8sub.synchCommandLine(1000,"setWaveAndFilter %f " % float(wl))
    time.sleep(30) 





# def clearCCD():
#    print "Clearing CCD "
#    raftsub = CCS.attachSubsystem(subsystem)
#    result = raftsub.synchCommandLine(1000,"setSequencerStart Clear")
#    result = raftsub.synchCommandLine(1000,"startSequencer")

# end function definitions #



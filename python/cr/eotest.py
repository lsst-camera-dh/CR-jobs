# eotest.py

from org.lsst.ccs.scripting import *
from REBlib import *
from REBPSlib import *
from ts7lib import *

# #################### Configuration ###########################
rebs=['greb0','greb1','wreb']
types = ['itl','itl','itl']

# sequencer files in use
seqdir = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/'
stdSeq = seqdir+'crtm_itl_shu_20180816.seq' # usual readout, with shutter
xedSeq = seqdir+'crtm_itl_xed_20180816.seq' # using XED instead of shutter
rghSeq = seqdir+'crtm_itl_ccdreset.seq'     # usual timng, but RG held high
rstSeq = seqdir+'crtm_itl_aspicreset.seq'   # usual timing, but ASPIC held reset
# illumination properties
wavelength = 500
fluence = 2830.0 #e-/pix/second
xrayTime = 180
# variable that determine which tests will be run
doSuperBias = 1
doDarkFrames = 1
doFe55 = 1
doNoise = 1
doSuperFlats = 1
doPhotonTransfer = 1
doLinear = 1
doLambda = 1
doPersist = 1
doPump = 1
doStability = 1
doGainSweep = 1
doSCTE = 1
doPCTE = 1
doOG = 1
doGDSweep = 0
# Default voltages
bssVolts = -50
serHiDefault = +5.0
serLoDefault = -5.0
parHiDefault = +3.0
parLoDefault = -8.0
rgHiDefault = +8.0
rgLoDefault = -2.0
odDefault = +26.0
gdDefault = +20.0
rdDefault = +13.0
ogDefault = -2.0

def startup():
#    for reb in rebs: rampDownHVBias(reb)
#    for reb in rebs: vrampHVBias(reb, 0, bssVolts, -5)
#    for reb in rebs: setBackBiasOff(reb)
#    for reb in rebs: hvbiasOff(reb)
#    for reb in rebs: ccdPowerDown(reb,'itl')
#    for reb in rebs: ccdPowerUp(reb,'itl')
#    for reb in rebs: hvbiasOn(reb)
#    for reb in rebs: setBackBiasOn(reb)
#    for reb in rebs: vsetHVBias(reb, bssVolts)
#    setWavelength(wavelength)
#    for reb in rebs: loadSeq(reb,stdSeq)
     print, 'Ready'

# ####################### Start of Program #############################

ts7FilamentOff()
startup()
for reb in rebs: loadSeq(reb,stdSeq)

if doSuperBias:
    imageCount = 50
    print "superBias:  Image Count: %4d " % imageCount
    for x in xrange(0, imageCount):   
        acquireBias("sbias_bias_%03d" % x)    

if doDarkFrames:
    dark_time = 500
    dark_count = 5 
    for x in xrange(0, dark_count):    
        acquireBias("dark_bias_%03d" % x)    
        acquireDark(dark_time, "dark_dark_%03d" % x)

if doFe55 :
    count = 5
    print 'Acquiring ',count,' fe55 exposures of ',xrayTime,' seconds'
    for reb in rebs: loadSeq(reb,xedSeq)
    for i in range(count):
        acquireBias("fe55_bias_%03d" % i)    
        acquireExposure(xrayTime, "fe55_fe55_%03d" % i)
        #acquireDark(xrayTime, "fe55_dark_%03d" % i)
    for reb in rebs: loadSeq(reb,stdSeq)

if doNoise :
    count = 3
    for reb in rebs: loadSeq(reb,rghSeq)  # with RG held high
    for i in range(count):
        files = acquireBias("rg_%03d" % i) 
    for reb in rebs: loadSeq(reb,rstSeq) # with ASPIC held reset
    for i in range(count):
        files = acquireBias("rst_%03d" % i)
    for reb in rebs: loadSeq(reb,stdSeq) # back to standard readout

if doSuperFlats:
    low_target = 1000.0
    low_expt   = low_target/float(fluence)
    low_count  = 50
    high_target = 50000.0
    high_expt  = high_target/float(fluence)
    high_count = 5
    print "Superflat: Exptime = %f  Image count = %d" % (low_expt,low_count)
    setWavelength(wavelength)
    for x in xrange(0, low_count):    
        acquireExposure(low_expt, "sflat_%03d_flat_L%03d" % (int(wavelength), x))
    print "Superflat: Exptime = %f  Image count = %d" % (high_expt,high_count)
    for x in xrange(0, high_count):
        acquireExposure(high_expt, "sflat_%03d_flat_H%03d" % (int(wavelength), x))

if doStability:
    count = 120
    delay = 100  # delay between image pairs, in seconds
    print "Stability: Integration time = %f  Image count = %d" % (expt,count)
    for reb in rebs: loadSeq(reb,xedSeq)
    for i in range(count):
        acquireExposure(xrayTime, "stabil_fe55_%03d" % i)
        time.sleep(delay)
    for reb in rebs: loadSeq(reb,stdSeq) # back to standard readout

if doPhotonTransfer:
    for etime in range(0, 1050, 50):
        exptime = etime / 100.0
        acquireBias( "flat_bias_%06.2fs_bias" % exptime)
        acquireExposure(exptime, "flat_flat_%06.2fs_flat1" % exptime)
        acquireExposure(exptime, "flat_flat_%06.2fs_flat2" % exptime)
    for etime in range(100, 1050, 50):
        exptime = etime / 10.0
        acquireBias( "flat_bias_%06.2fs_bias" % exptime)
        acquireExposure(exptime, "flat_flat_%06.2fs_flat1" % exptime)
        acquireExposure(exptime, "flat_flat_%06.2fs_flat2" % exptime)

if doLinear:
    for etime in range(0, int(120000.0/float(fluence)), 2):
        acquireBias("linearity_bias_%06.2fs" % etime)
        acquireExposure(etime, "linearity_flat_%06.2fs" % etime)

if doLambda:
    waves = [ 320, 330, 350, 370, 400, 430, 450, 500, 550, 570, 600, 620, 630, 650, 670, 700, 720, 750, 770, 800, 830, 870, 900, 920, 960,1000,1030,1050,1080,1100]
    times = [95.3,67.3,40.3,21.4,10.6,8.68,6.78,7.21,7.44,7.44,7.92,7.68,8.23,8.60,9.23,10.6,11.2,11.1,13.6,14.8,5.50,12.1,5.80,3.90,14.5,20.4,93.6, 130, 314,500]
    for i in range(30):
        wl = waves[i]
        etime = times[i]
        setWavelength(waves[i])
        acquireBias( "lambda_bias_%03d" % i)
        acquireExposure(etime, "lambda_flat_%04d_%03d" % (waves[i],i))
    setWavelength(wavelength)

if doPersist:
    for i in range(5):
        acquireBias( "persistence_bias_%03d" % i)
    exptime = 150000.0/float(fluence)
    acquireExposure(exptime, "persistence_flat")
    for i in range(12):
        acquireDark(15, "persistence_dark_%03d" % i)
        
if doPump:
    for i in range(25):
        acquireBias( "trap_bias_%03d" % i)
    exptime = 20000.0/float(fluence)
    acquireExposure(exptime, "trap_flat")
    acquirePumped(exptime, "trap_pump")

if doSCTE:
    Lo_Start = -5.00
    Lo_End   = -3.00
    Lo_Step  =  0.50
    Range_Start = +7.00
    Range_End   = +10.00
    Range_Step  =  0.50
    og_Start = -3.00
    og_End   = 1.00
    og_Step  = 0.50
    imageCount = 1
    etimes = [50000.0/float(fluence)]
    Lo_Volts = Lo_Start
    while (Lo_Volts <= Lo_End):
        Range = Range_Start
        while (Range <= Range_End):
            Hi_Volts = Lo_Volts + Range
            for reb in rebs: vsetSerLo(reb, Lo_Volts)
            for reb in rebs: vsetSerHi(reb, Hi_Volts)
            og_Volts = og_Start
            while (og_Volts <= og_End):
                for reb in rebs: vsetOG(reb, og_Volts)
                for exptime in etimes:
                    for i in range(0, imageCount):
                        fbase = ("scte_%05.2f_%05.2f_%05.2f_%03i" % (Lo_Volts, Hi_Volts, og_Volts, i))
                        acquireExposure(exptime, fbase)
                og_Volts = og_Volts + og_Step
            Range = Range + Range_Step
        Lo_Volts = Lo_Volts + Lo_Step
    for reb in rebs: vsetSerLo(reb, serLoDefault)
    for reb in rebs: vsetSerHi(reb, serHiDefault)
    for reb in rebs: vsetOG(reb, ogDefault)
    print "Serial CTE sweep complete."         

if doOG :
    ogStart = -4.00
    ogEnd   = 2.00
    ogStep  = 0.50
    target = 50000.0
    exptime = target/float(fluence)
    ogVolts = ogStart
    while (ogVolts <= ogEnd):
        for reb in rebs: vsetOG(reb, ogVolts)
        acquireExposure(exptime, "og_flat_%05.2f" % ogVolts)
        for reb in rebs: loadSeq(reb,xedSeq)
        acquireExposure(xrayTime, "og_fe55_%05.2f" % ogVolts)
        for reb in rebs: loadSeq(reb,stdSeq)
        ogVolts = ogVolts + ogStep
    for reb in rebs: vrampOG(reb, ogVolts, ogDefault, 0.5)
    print "OG CTE sweep complete."

if doPCTE :
    Lo_Start = -9.00
    Lo_End   = -4.00
    Lo_Step  =  0.50
    Dphi_Start = 7.0
    Dphi_End = 10.0
    Dphi_Step = 1.0
    target = 50000.0
    exptime = target/float(fluence)
    Lo_Volts = Lo_Start
    Dphi_Volts = Dphi_Start
    while (Lo_Volts <= Lo_End):
        for reb in rebs: vsetParLo(reb, Lo_Volts)
        Dphi_Volts = Dphi_Start
        while (Dphi_Volts <= Dphi_End):
            for reb in rebs: vsetDphi(reb, Dphi_Volts)
            Hi_Volts = Lo_Volts + Dphi_Volts
            fbase = ("pcte_%05.2f_%05.2f" % (Lo_Volts, Hi_Volts))
            acquireExposure(exptime, fbase)
            Dphi_Volts = Dphi_Volts + Dphi_Step
        Lo_Volts = Lo_Volts + Lo_Step
    for reb in rebs: vsetParLo(reb, parLoDefault)
    for reb in rebs: vsetParHi(reb, parHiDefault)
    print "Parallel CTE sweep complete."

#if doGDSweep :
#    gdLow = 18
#    gdHigh = 26
#    gdStep = 1.0
#    etimes = [0,10,20,60]
#    gdVolts = gdLow
#    while (gdVolts <= gdHigh):
#        vsetGD(reb,gdVolts)        
#        for exptime in etimes :        
#            fbase = ("gd_%05.2f_%06.2fs_flat1" % (gdVolts, exptime))
#            acquireExposure(exptime, fbase)
#            fbase = ("gd_%05.2f_%06.2fs_flat2" % (gdVolts, exptime))
#            acquireExposure(exptime, fbase)
#        gdVolts = gdVolts + gdStep

if doGainSweep :
    etimes = [20000.0/float(fluence)]
    odLow  = 25.0
    odHigh = 29.0
    odStep = 0.25
    rdLow  = 12.0
    rdHigh = 14.0
    rdStep = 0.25
    odLowLimit  = 21.0 
    odHighLimit = 30.0
    rdLowLimit  = 8.0 
    rdHighLimit = 18.0
    odVolts = odLow
    while (odVolts <= odHigh):
        if (odVolts < odLowLimit) or (odVolts > odHighLimit):
            break
        rdVolts = rdLow   
        while (rdVolts <= rdHigh):
            if (rdVolts < rdLowLimit) or (rdVolts > rdHighLimit):
                break
            for reb in rebs: vsetRD(reb, rdVolts)
            for reb in rebs: vsetOD(reb, odVolts)
            for exptime in etimes :        
                for reb in rebs: loadSeq(reb,xedSeq)
                fbase = ("gain_%05.2f_%05.2f_fe55" % (odVolts, rdVolts ))
                acquireExposure(xrayTime, fbase)
                for reb in rebs: loadSeq(reb,stdSeq)
                fbase = ("gain_%05.2f_%05.2f_flat1" % (odVolts, rdVolts ))
                acquireExposure(exptime, fbase)
                fbase = ("gain_%05.2f_%05.2f_flat2" % (odVolts, rdVolts))
                acquireExposure(exptime, fbase)
            rdVolts = rdVolts + rdStep
        odVolts = odVolts + odStep
    for reb in rebs: vrampRD(reb, rdVolts, rdDefault, 0.5)
    for reb in rebs: vrampOD(reb, odVolts, odDefault, 0.5)


ts7FilamentOff()


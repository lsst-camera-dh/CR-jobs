# eotest.py

from org.lsst.ccs.scripting import *
from REBlib import *
# from REBtest import *

dataDir = getDataDir()
prefix = getPrefix()
wreb ='itl'
greb ='itl'
teststand = 'ts5'
wavelength = 500
fluence = 2830.0 #e-/pix/second


#reb = 'wreb'
#reb = 'greb'
reb = 'both'

doSuperBias = 0
doDarkFrames = 0
doSuperFlats = 0
doPhotonTransfer = 0
doLinear = 0
doLambda = 0
doPersist = 0
doPump = 0
doGainSweep = 1
doSCTE = 0
doPCTE = 0
doStability = 0
doGDSweep = 0
doGainRamps = 0
doLinRamps = 0

seqfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_20180625.seq'
xedfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_xed_20180630.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)

# initialize
def setDefaults():
    if reb == 'greb':
        ccdPowerDown('w','itl')
        if greb == 'e2v': 
            ccdPowerUp('g0','e2v')
            ccdPowerUp('g1','e2v')
        else:
            ccdPowerUp('g0','itl')
            ccdPowerUp('g1','itl')
    elif reb == 'wreb':
        ccdPowerUp('w','itl')
        if greb == 'e2v': 
            ccdPowerDown('g0','e2v')
            ccdPowerDown('g1','e2v')
        else:
            ccdPowerDown('g0','itl')
            ccdPowerDown('g1','itl')
    elif reb == 'both':
        if greb == 'e2v': 
            ccdPowerUp('g0','e2v')
            ccdPowerUp('g1','e2v')
        else:
            ccdPowerUp('g0','itl')
            ccdPowerUp('g1','itl')
        ccdPowerUp('w','itl')
    else:
        print 'REB not recognized'
    if teststand == 'ts8': 
        setWavelength(wavelength)

# bias frames
if doSuperBias:
    setDefaults()
    imageCount = 100
    print "superBias:  Image Count: %4d " % imageCount
    for x in xrange(0, imageCount):   
        acquireBias("bias_bias_%03d" % x)    

# super flats
if doSuperFlats:
    setDefaults()
    wl = 500
    low_target = 1000.0
    low_expt   = low_target/float(fluence)
    low_count  = 50
    high_target = 50000.0
    high_expt  = high_target/float(fluence)
    high_count = 5
    print "Superflat: Exptime = %f  Image count = %d" % (low_expt,low_count)
    for x in xrange(0, low_count):    
        acquireExposure(low_expt, "sflat_%03d_flat_L%03d" % (int(wl), x))
    print "Superflat: Exptime = %f  Image count = %d" % (high_expt,high_count)
    for x in xrange(0, high_count):
        acquireExposure(high_expt, "sflat_%03d_flat_H%03d" % (int(wl), x))
    setDefaults()

# stability test
if doStability:
    setDefaults()
    target = 20000.0
    expt = target/float(fluence)
    count = 120
    delay = 50  # delay between image pairs, in seconds
    print "Stability: Exptime = %f  Image count = %d" % (expt,count)
    for i in xrange(0, count):    
        acquireBias( "stabil_bias_%03d" % i)
        acquireExposure(expt, "stabil_flat1_%03d" % i)
        acquireExposure(expt, "stabil_flat2_%03d" % i)
        time.sleep(delay)

# photon transfer
if doPhotonTransfer:
    setDefaults()
#    targets = [0,100,200,300,400,500,600,700,800,900,1000,1200,1300,1400,1500,1600,1700,1800,1900,2000,
#              2200,2400,2600,2800,2900,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,
#              9500,10000,12000,14000,16000,18000,20000,25000,30000,35000,40000,45000,50000,55000,60000,
#              65000,70000,75000,80000,85000,86000,87000,88000,89000,90000,91000,92000,93000,94000,95000,
#              100000,110000,120000,130000,140000,150000,160000,170000,180000,190000,200000]
#
#    for i = range(len(targets)):
#        etime = float(targets[i])/float(fluence)
#        acquireBias( "flat_bias_%06.2fs_bias" % exptime)
#        acquireExposure(exptime, "flat_flat_%06.2fs_flat1" % exptime)
#        acquireExposure(exptime, "flat_flat_%06.2fs_flat2" % exptime)

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

# linearity 
if doLinear:
    setDefaults()
    for etime in range(0, int(120000.0/float(fluence)), 2):
        acquireBias("linearity_bias_%06.2fs" % etime)
        acquireExposure(etime, "linearity_flat_%06.2fs" % etime)

# lambda
if doLambda:
    setDefaults()
    waves = [ 320, 330, 350, 370, 400, 430, 450, 500, 550, 570, 600, 620, 630, 650, 670, 700, 720, 750, 770, 800, 830, 870, 900, 920, 960,1000,1030,1050,1080,1100]
    times = [95.3,67.3,40.3,21.4,10.6,8.68,6.78,7.21,7.44,7.44,7.92,7.68,8.23,8.60,9.23,10.6,11.2,11.1,13.6,14.8,5.50,12.1,5.80,3.90,14.5,20.4,93.6, 130, 314,1027]
    for i in range(30):
        wl = waves[i]
        etime = times[i]
        setWavelength(waves[i])
        acquireBias( "lambda_bias_%03d" % i)
        acquireExposure(etime, "lambda_flat_%04d_%03d" % (waves[i],i))
    setWavelength(wavelength)

# persist
if doPersist:
    setDefaults()
    for i in range(5):
        acquireBias( "persistence_bias_%03d" % i)
    exptime = 150000.0/float(fluence)
    acquireExposure(exptime, "persistence_flat")
    for i in range(12):
        acquireDark(15, "persistence_dark_%03d" % i)
        
# ppump
if doPump:
    setDefaults()
    for i in range(25):
        acquireBias( "trap_bias_%03d" % i)
    exptime = 20000.0/float(fluence)
    acquireExposure(exptime, "trap_flat")
    acquirePumped(exptime, "trap_pump")

# dark frames
if doDarkFrames:
    setDefaults()
    dark_time = 500
    dark_count = 5 
    for x in xrange(0, dark_count):    
        acquireBias("dark_bias_%03d" % x)    
        acquireDark(dark_time, "dark_dark_%03d" % x)

# serial CTE sweep
if doSCTE:
    setDefaults()
    #if reb == 'wreb':
    Lo_Start = -7.00
    Lo_End   = -3.00
    Lo_Step  =  0.50
    Range_Start = +8.00
    Range_End   = +11.00
    Range_Step  =  0.50
    og_Start = -3.00
    og_End   = 1.00
    og_Step  = 0.50
    #else:    
    #    Lo_Start = 0.00
    #    Lo_End   = 2.00
    #    Lo_Step  =  0.50
    #    Range_Start = +7.00
    #    Range_End   = +10.00
    #    Range_Step  =  0.50
    #    og_Start = 2.00
    #    og_End   = 5.00
    #    og_Step  = 0.50
    # Lo_LoLimit  = -9.50 
    # Lo_HiLimit  =  0.00
    # Hi_LoLimit  =  0.00
    # Hi_HiLimit  = +8.00
    
    imageCount = 1
    etimes = [50000.0/float(fluence)]
    Lo_Volts = Lo_Start
    while (Lo_Volts <= Lo_End):
        Range = Range_Start
        while (Range <= Range_End):
            Hi_Volts = Lo_Volts + Range
            vsetSerLo(reb,Lo_Volts)
            vsetSerHi(reb,Hi_Volts)
            og_Volts = og_Start
            while (og_Volts <= og_End):
                vsetOG(reb,og_Volts)
                for exptime in etimes:
                    for i in range(0, imageCount):
                        fbase = ("scte_%05.2f_%05.2f_%05.2f_%03i" % (Lo_Volts, Hi_Volts, og_Volts, i))
                        acquireExposure(exptime, fbase)
                og_Volts = og_Volts + og_Step
            Range = Range + Range_Step
        Lo_Volts = Lo_Volts + Lo_Step
    setDefaults()
    print "Serial CTE sweep complete."         

# parallel CTE sweep
if doPCTE :
    #setDefaults()
    #if reb == 'wreb':
    #Lo_Start = -9.00
    #Lo_End   = -5.00
    #Lo_Step  =  0.5
    #Dphi = 10.0
    #target = 50000.0
    #exptime = target/float(fluence)
    #Lo_LoLimit  = -10.00
    #Lo_HiLimit  =  0.00
    #Hi_LoLimit  =  0.00
    #Hi_HiLimit  = +10.00
    #Lo_Volts = Lo_Start
    #while (Lo_Volts <= Lo_End):
    #    vsetParLo(reb,Lo_Volts)
    #    Hi_Volts = Lo_Volts + Dphi
    #    fbase = ("pcte_%05.2f_%05.2f" % (Lo_Volts, Hi_Volts))
    #    acquireExposure(exptime, fbase)
    #    Lo_Volts = Lo_Volts + Lo_Step
    #setDefaults()
    print "Parallel CTE sweep complete."

# GD sweep
if doGDSweep :
    setDefaults()
#    if reb == 'wreb'
#        gdLow = 18
#        gdHigh = 26
#        gdStep = 1.0
#    else:
#        gdLow = 18
#        gdHigh = 26
#        gdStep = 1.0
#
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
#    setDefaults()

# gain sweep
if doGainSweep :
    setDefaults()
    #etimes = [20000.0/float(fluence)]
    etimes = [2]
    #if reb == 'wreb':
    odLow  = 24.0
    odHigh = 29.0
    odStep = 0.25
    rdLow  = 11.0
    rdHigh = 14.0
    rdStep = 0.25
    odLowLimit  = 21.0 
    odHighLimit = 30.0
    rdLowLimit  = 8.0 
    rdHighLimit = 18.0
    #else:
    #    odLow  = 28.0
    #    odHigh = 31.0
    #    odStep = 0.25
    #    rdLow  = 16.0
    #    rdHigh = 20.0
    #    rdStep = 0.25
    #    odLowLimit  = 21.0 
    #    odHighLimit = 30.0
    #    rdLowLimit  = 8.0 
    #    rdHighLimit = 18.0
    
    odVolts = odLow
    while (odVolts <= odHigh):
        if (odVolts < odLowLimit) or (odVolts > odHighLimit):
            break
        rdVolts = rdLow   
        while (rdVolts <= rdHigh):
            if (rdVolts < rdLowLimit) or (rdVolts > rdHighLimit):
                break
            vsetRD('w',rdVolts)
            vsetOD('w',odVolts)        
            vsetRD('g',rdVolts)
            vsetOD('g',odVolts)        
            for exptime in etimes :        
                fbase = ("gain_%05.2f_%05.2f_fe55" % (odVolts, rdVolts ))
                acquireExposure(exptime, fbase)
                #fbase = ("gain_%05.2f_%05.2f_flat1" % (odVolts, rdVolts ))
                #acquireExposure(exptime, fbase)
                #fbase = ("gain_%05.2f_%05.2f_flat2" % (odVolts, rdVolts))
                #acquireExposure(exptime, fbase)
            rdVolts = rdVolts + rdStep
        odVolts = odVolts + odStep
    setDefaults()

# gain ramps
if doGainRamps:
    setDefaults()
    rowDelay = 3500   # time to pause between rows, in usec
    #if reb == 'wreb':
    odLow  = 24.0
    odHigh = 29.0
    odStep = 0.25
    rdLow  = 11.0
    rdHigh = 14.0
    rdStep = 0.25
    odLowLimit  = 21.0 
    odHighLimit = 30.0
    rdLowLimit  = 8.0 
    rdHighLimit = 18.0
    #else:
    #    odLow  = 28.0
    #    odHigh = 31.0
    #    odStep = 0.25
    #    rdLow  = 16.0
    #    rdHigh = 20.0
    #    rdStep = 0.25
    #    odLowLimit  = 24.0 
    #    odHighLimit = 32.0
    #    rdLowLimit  = 14.0 
    #    rdHighLimit = 22.0

    odVolts = odLow
    while (odVolts <= odHigh):
        if (odVolts < odLowLimit) or (odVolts > odHighLimit):
             break
        rdVolts = rdLow   
        while (rdVolts <= rdHigh):
            if (rdVolts < rdLowLimit) or (rdVolts > rdHighLimit):
                break
            vsetRD(reb,rdVolts)
            vsetOD(reb,odVolts)       
            acquireRamp(rowDelay, "gramp_%05.2f_%05.2f_ramp1" % (odVolts, rdVolts))
            acquireRamp(rowDelay, "gramp_%05.2f_%05.2f_ramp2" % (odVolts, rdVolts))
            rdVolts = rdVolts + rdStep
        odVolts = odVolts + odStep
    setDefaults()

# low linearity ramps
if doLinRamps:
    setDefaults()
    linCount = 100
    rowDelay = 1500   # time to pause between rows, in usec
    for x in xrange(0, linCount):
        acquireRamp(rowDelay, "lramp_%03d" % x)



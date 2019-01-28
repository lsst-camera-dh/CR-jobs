# crtmInit.py
# Initialize the CRTM
import time
from org.lsst.ccs.scripting import *
from REBlib import *

guiderType = 'ITL'

# Setting CCD type does not work yet, don't do it
#setCCD('ITL')
#ccdtype = getCCD()
#print "CCD type = ",ccdtype

# Configure the ASPICs on the WREB
loadAspics('wreb')
loadAspics('greb')
#aspicGain('w',1)
#aspicRc('w',13)
#aspicGain('g',1)
#aspicRc('g',13)

# configure the sequencer
#seqfile = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/crtm_itl_shu_20180630.seq'
#seqfile = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/crtm_itl_20180625.seq'
seqfile = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/crtm_itl_xed_20180630.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)

# set the default CCD clock volatges
print "Make sure Back Bias is off..."
setBackBiasOff('w')
print 'WREB Back bias: ', getBackBiasState('w')
setBackBiasOff('g')
print 'GREB Back bias: ', getBackBiasState('g')
ccdPowerUp('w', 'ITL')
ccdPowerUp('g0', guiderType)
ccdPowerUp('g1', guiderType)

# Setting CCD type does not work yet, don't do it
setCCD('ITL')
ccdtype = getCCD()


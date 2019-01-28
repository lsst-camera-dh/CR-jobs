# warmTest.py
from org.lsst.ccs.scripting import *
from REBlib import *

if len(sys.argv) < 2 or sys.argv[1] == '': 
    count = 1
else:
    count = int(sys.argv[1])

# set the default CCD clock volatges
print "Make sure Back Bias is off..."
setBackBiasOff('w')
print 'WREB Back bias: ',getBackBiasState('w')
setBackBiasOff('g')
print 'GREB Back bias: ',getBackBiasState('g')
#ccdPowerUp('w','ITL')
#ccdPowerUp('g0','ITL')
#ccdPowerUp('g1','ITL')

seqfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_20180625.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)
fbase="warm"
for i in range(count):
    files = acquireBias(fbase+"_%03d" % i)

seqfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_ccdreset.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)
fbase="rg"
for i in range(count):
    files = acquireBias(fbase+"_%03d" % i)

seqfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_aspicreset.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)
fbase="rst"
for i in range(count):
    files = acquireBias(fbase+"_%03d" % i)

seqfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_20180625.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)
fbase="exp"
for i in range(count):
    files = acquireExposure(10.0, fbase+"_%03d" % i)

#ccdPowerDown('w','ITL')
#ccdPowerDown('g0','e2v')
#ccdPowerDown('g1','e2v')


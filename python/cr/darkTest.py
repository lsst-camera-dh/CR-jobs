# warmTest.py
from org.lsst.ccs.scripting import *
from REBlib import *

if len(sys.argv) < 2 or sys.argv[1] == '': 
    count = 1
else:
    count = int(sys.argv[1])

# ts7-2cr/VQMonitor setFilamentOff

# set the default CCD clock volatges

seqfile = '/gpfs/slac/lsst/fs1/g/data/R_and_D/cr/sequences/crtm_itl_20180625.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)

setBackBiasOn('w')
setBackBiasOn('g')

fbase="fe55_bias"
for i in range(count):
    files = acquireBias(fbase+"_%03d" % i)

fbase="fe55_fe55"
for i in range(count):
    files = acquireExposure(60.0, fbase+"_%03d" % i)
for i in range(count):
    files = acquireExposure(300.0, fbase+"_%03d" % i)

fbase="fe55_dark"
for i in range(count):
    files = acquireDark(60.0, fbase+"_%03d" % i)
for i in range(count):
    files = acquireDark(300.0, fbase+"_%03d" % i)

fbase="dark_bias"
for i in range(count):
    files = acquireBias(fbase+"_%03d" % i)

fbase="dark_dark"
for i in range(count):
    files = acquireDark(500.0, fbase+"_%03d" % i)

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



# loadXed.py  
# load the sequencer file that controls the XEDs
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 0

seqdir = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/'
seqfile = 'crtm_itl_xed_20180816.seq'
if verbose: print 'Loading sequencer file ',seqfile

loadSeq('w',seqdir+seqfile)
loadSeq('g',seqdir+seqfile)


# crtmInit.py
# Initialize the CRTM
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 0

seqdir = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/'
seqfile = 'crtm_itl_shu_20180816.seq'
if verbose: print 'Loading sequencer file ',seqfile

loadSeq('w',seqdir+seqfile)
loadSeq('g',seqdir+seqfile)



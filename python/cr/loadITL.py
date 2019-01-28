# crtmInit.py
# Initialize the CRTM
from org.lsst.ccs.scripting import *
from REBlib import *

seqdir = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/'

#seqfile = seqdir+'crtm_itl_20180625.seq'
#seqfile = seqdir+'crtm_itl_shu_20180630.seq'
seqfile = seqdir+'crtm_itl_shu_20180816.seq'
#seqfile = seqdir+'crtm_itl_ccdreset.seq'
#seqfile = seqdir+'crtm_itl_aspicreset.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)



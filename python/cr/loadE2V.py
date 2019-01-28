# crtmInit.py
# Initialize the CRTM
from org.lsst.ccs.scripting import *
from REBlib import *

#seqfile = '/lsst/ccs/sequences/seq-e2v-2s_rghi.seq'
seqfile = '/lsst/ccs/sequences/seq-e2v-2s.seq'
#seqfile = '/lsst/ccs/sequences/crtm_itl_20180515.seq'
#seqfile = '/lsst/ccs/sequences/rghi_noclks.seq'
#seqfile = '/lsst/ccs/sequences/clamp.seq'
print 'Loading sequencer file ',seqfile
loadSeq('w',seqfile)
loadSeq('g',seqfile)



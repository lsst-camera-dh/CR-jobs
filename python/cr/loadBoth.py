# crtmInit.py
# Initialize the CRTM
from org.lsst.ccs.scripting import *
from REBlib import *

#e2v = '/lsst/ccs/sequences/seq-e2v-2s_rghi.seq'
e2v = '/lsst/ccs/sequences/seq-e2v-2s.seq'
itl = '/lsst/ccs/sequences/crtm_itl_20180515.seq'

#print 'Loading sequencer file ',itl,' into WREB'
#loadSeq('w',itl)
print 'Loading sequencer file ',e2v,' into GREB'
loadSeq('g',e2v)

print 'Loading sequencer file ',itl,' into WREB'
loadSeq('w',itl)


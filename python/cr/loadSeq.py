# crtmInit.py
# Initialize the CRTM
from org.lsst.ccs.scripting import *
from REBlib import *

verbose = 1

if len(sys.argv) < 2 or sys.argv[1] == '':
    seqfile = 'crtm_itl_shu_20180816.seq'
    #seqfile = 'crtm_itl_20180625.seq'
    #seqfile = 'crtm_itl_20180625.seq'
    #seqfile = 'crtm_itl_shu_20180630.seq'
    #seqfile = 'crtm_itl_xed_delay_20180630.seq'
    #seqfile = 'crtm_itl_ccdreset.seq'
    #seqfile = 'crtm_itl_aspicreset.seq'
else:
    seqfile = sys.argv[1]

seqdir = '/gpfs/slac/lsst/fs1/g/data/cr/sequences/'

sfile = seqdir + seqfile
print 'Loading sequencer file ',sfile
loadSeq('w',sfile)
loadSeq('g',sfile)



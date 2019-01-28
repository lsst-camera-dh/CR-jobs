# pxfer.py

from org.lsst.ccs.scripting import *
from REBlib import *
# from REBtest import *

dataDir = getDataDir()
prefix = getPrefix()
wavelength = 500
fluence = 2832.0 #e-/pix/second

#reb = 'wreb'
reb = 'greb'

# initialize
setWavelength(wavelength)

for Dphi in [8.0,8.5,9.0,9.5,10.0,10.5,11.0]:
     vsetDphi(reb, Dphi)
     targets = [0,100,200,300,400,500,600,700,800,900,1000,1200,1300,1400,1500,1600,1700,1800,1900,2000,
               2200,2400,2600,2800,2900,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,
               9500,10000,12000,14000,16000,18000,20000,25000,30000,35000,40000,45000,50000,55000,60000,
               65000,70000,75000,80000,85000,86000,87000,88000,89000,90000,91000,92000,93000,94000,95000,
               100000,110000,120000,130000,140000,150000,160000,170000,180000,190000,200000]
     for i in range(len(targets)):
         etime = float(targets[i])/float(fluence)
         acquireExposure(etime, "pxfer_%04.1f_%06.2fs_flat1" % (Dphi,etime))
         acquireExposure(etime, "pxfer_%04.1f_%06.2fs_flat2" % (Dphi,etime))


# eotest.py

from org.lsst.ccs.scripting import *
from REBlib import *

dataDir = getDataDir()
prefix = getPrefix()
ccd ='itl'

setBackBiasOn('w')
setBackBiasOn('g')

od_default = 26.5
rd_default = 12.5

etimes = [120]

if ccd == 'itl':
    odLow  = 25.0
    odHigh = 28.0
    odStep = 0.50
    rdLow  = 12.0
    rdHigh = 14.0
    rdStep = 0.50
    odLowLimit  = 21.0
    odHighLimit = 30.0
    rdLowLimit  = 10.0
    rdHighLimit = 16.0
else:
    odLow  = 28.0
    odHigh = 31.0
    odStep = 0.50
    rdLow  = 17.0
    rdHigh = 20.0
    rdStep = 0.50
    odLowLimit  = 25.0 
    odHighLimit = 32.0
    rdLowLimit  = 14.0 
    rdHighLimit = 21.0

odVolts = odLow
while (odVolts <= odHigh):
    if (odVolts < odLowLimit) or (odVolts > odHighLimit):
        break
    rdVolts = rdLow
    while (rdVolts <= rdHigh):
        if (rdVolts < rdLowLimit) or (rdVolts > rdHighLimit):
            break
        vsetRD('w',rdVolts)
        vsetOD('w',odVolts)
        vsetRD('g0',rdVolts)
        vsetOD('g0',odVolts)
        vsetRD('g1',rdVolts)
        vsetOD('g1',odVolts)
        for exptime in etimes :
            fbase = ("gain_%05.2f_%05.2f_fe55" % (odVolts, rdVolts ))
            acquireExposure(exptime, fbase)
        rdVolts = rdVolts + rdStep
    odVolts = odVolts + odStep
vsetRD('w',rd_default)
vsetOD('w',od_default)
vsetRD('g0',rd_default)
vsetOD('g0',od_default)
vsetRD('g1',rd_default)
vsetOD('g1',od_default)


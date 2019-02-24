#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import glob
import time
import lsst.eotest.image_utils as imutils
#import pyfits as pf
#import astropy.io.fits as pf

def measured_flux(filename,seqno=0, fluxcal_time=2.):

#        for fits_file in fits_files:
#            print("fits_file = ",fits_file)
#            print("self.md.cwd = ",self.md.cwd)
#            file_path = glob.glob(os.path.join(self.md.cwd, '*', fits_file))[0]

    file_path = filename

    avg = 0.0
    segcount = 0
    flux_sum = 0.0
    for i in range(16):
        md = imutils.Metadata(file_path, i+1)
        avg = avg + md.get('AVERAGE') - md.get('AVGBIAS')
        segcount = segcount+1
    avg = avg / segcount

    flux_sum += avg
#    return flux_sum/len(fits_files)
    return flux_sum

#print("123.0")
#print("determining stats for fits file - ",sys.argv[1])
print(measured_flux(sys.argv[1]))

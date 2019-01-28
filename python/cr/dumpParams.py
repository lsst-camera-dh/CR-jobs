# DumpParams.py
# 

import time
from org.lsst.ccs.scripting import *
from REBlib import *


val = getSeqParam("PreCols")  # Number of columns to skip before readout window, including prescan
print val
#val = getSeqParam("ReadCols") #     # Number of columns to read
#val = getSeqParam("PostCols") #     # Number of columns to discard after window (it is up to the user that total columns = 576)
#val = getSeqParam("OverCols") #      # Number of columns acquired after line is read for baseline subtraction
#val = getSeqParam("ReadCols2") #     # Number of columns in second part of ROI if split
#val = getSeqParam("ExposureTime") # # Duration of exposure in units of 25 ms
#val = getSeqParam("PreRows") #       # Number of rows to skip before window
#val = getSeqParam("ReadRows") #     # Number of rows of the window
#val = getSeqParam("PostRows") #     # Number of rows after window (it is up to the user that total lines = 2048)
#val = getSeqParam("ClearCount") #   # Number of full CCD clears executed by the Clear main
#val = getSeqParam("CleaningNumber") #  Number of full CCD clears before acquiring a frame

#val = getSeqParam("FlushTime") #   # Repetitions of FlushPixel function during FlushRegister
#val = getSeqParam("PumpNumber") #  # Number of parallel pumps




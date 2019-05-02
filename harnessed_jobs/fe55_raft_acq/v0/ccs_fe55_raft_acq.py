"""
Jython script to run Fe55 acquisitions at TS8.
"""
from eo_acquisition import EOAcquisition, AcqMetadata, logger
from ccs_scripting_tools import CcsSubsystems, CCS
import time

class Fe55Acquisition(EOAcquisition):
    """
    EOAcquisition subclass to take the Fe55 dataset.
    """
    def __init__(self, seqfile, acq_config_file, metadata, subsystems,
                 ccd_names, logger=logger):
        super(Fe55Acquisition, self).__init__(seqfile, acq_config_file, "FE55",
                                              metadata, subsystems, ccd_names,
                                              logger=logger)

    def run(self):
        """
        Take the Fe55 data.
        """
        openShutter = False
        actuateXed = True
        image_type = "FE55"

#        pdusub = CCS.attachSubsystem("ts7-2cr/PDU20")
#        pdusub.sendSynchCommand("forceOutletOn XED-CONTROL")
#        time.sleep(10.0)

#        self.sub.mono.sendSynchCommand("closeShutter")


        seqno = 0
        for tokens in self.instructions:
            exptime = float(tokens[1])
            nframes = int(tokens[2])
            for iframe in range(nframes):
                self.image_clears()
                self.bias_image(seqno)
                self.take_image(seqno, exptime, openShutter, actuateXed,
                                image_type)
                seqno += 1

#        pdusub.sendSynchCommand("forceOutletOff XED-CONTROL")
        self.sub.mono.sendSynchCommand("openShutter")


if __name__ == '__main__':
    metadata = AcqMetadata(cwd=tsCWD, raft_id=UNITID, run_number=RUNNUM)
    acq = Fe55Acquisition(sequence_file, rtmacqcfgfile, metadata, subsystems,
                          ccd_names)
    acq.run()

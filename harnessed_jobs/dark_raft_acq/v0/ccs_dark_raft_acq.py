"""
Jython script to acquire dark exposure dataset (used to find bright defects and
to estimate dark current).
"""
from eo_acquisition import EOAcquisition, AcqMetadata, logger
from ccs_scripting_tools import CcsSubsystems, CCS

class DarkAcquisition(EOAcquisition):
    """
    EOAcquisition subclass to acquire dark exposure dataset.
    """
    def __init__(self, seqfile, acq_config_file, metadata, subsystems,
                 ccd_names, logger=logger):
        print("seqfile = ",seqfile)
        print("acq_config_file = ",acq_config_file)
        super(DarkAcquisition, self).__init__(seqfile, acq_config_file, "DARK",
                                              metadata, subsystems, ccd_names,
                                              logger=logger)

    def run(self):
        print("chk00")
        """
        Take the dark exposures.
        """
        openShutter = False
        actuateXed = False
        image_type = "DARK"

#        pdusub = CCS.attachSubsystem("ts7-2cr/PDU20")
#        pdusub.sendSynchCommand("forceOutletOff XED-CONTROL")

        print("chk1")
        for tokens in self.instructions:
            print("chk2")
            exptime = float(tokens[1])
            frame_count = int(tokens[2])
            for seqno in range(frame_count):
                self.image_clears()
                self.bias_image(seqno)
                self.take_image(seqno, exptime, openShutter, actuateXed,
                                image_type)

if __name__ == '__main__':
    metadata = AcqMetadata(cwd=tsCWD, raft_id=UNITID, run_number=RUNNUM)
    print("m0")
    print("sequence_file = ",sequence_file)
    acq = DarkAcquisition(sequence_file, rtmacqcfgfile, metadata, subsystems,
                          ccd_names)
    print("m1")
    acq.run()

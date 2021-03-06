"""
Test Stand 8 electro-optical acquisition jython scripting module.
"""
from __future__ import print_function
import os
import sys
import glob
import subprocess
import time

#import pyfits as pf
#import lsst.eotest.image_utils as imutils
from collections import namedtuple
import logging
from java.time import Duration
from REBlib import acquireExposureMaster
import re
try:
    import java.lang
except ImportError:
    print("could not import java.lang")
from ccs_scripting_tools import CcsSubsystems, CCS
from ts8_utils import set_ccd_info, write_REB_info

__all__ = ["hit_target_pressure", "EOAcquisition",
           "PhotodiodeReadout", "EOAcqConfig", "AcqMetadata", "logger"]

CCS.setThrowExceptions(True)
#CCS.setDefaultTimeout(3000.00)

logging.basicConfig(format="%(message)s",
                    level=logging.INFO,
                    stream=sys.stdout)
logger = logging.getLogger()

def hit_target_pressure(vac_sub, target, wait=5, tmax=7200, logger=logger):
    """
    Function to wait until target pressure in vacuum gauge subsystem
    is attained.

    Parameters
    ----------
    vac_sub : CCS subsystem
        The vacuum subsystem.
    target : float
        The target pressure (torr).
    wait : float, optional
        The wait time (sec) between pressure reads.  Default: 5
    tmax : float, optional
        The maximum time (sec) to allow for the target pressure to be attained.
        Default: 7200
    logger : logging.Logger
        The logger object.
    """
    tstart = time.time()
    pressure = vac_sub.sendSynchCommand("readPressure")
    while pressure > target or pressure < 0:
        logger.info("time = %s, pressure = %f", time.time(), pressure)
        if (time.time() - tstart) > tmax:
            raise RuntimeError("Exceeded allowed pump-down time for "
                               + "target pressure %s" % target)
        time.sleep(wait)
        pressure = vac_sub.sendSynchCommand("readPressure")

AcqMetadata = namedtuple('AcqMetadata', 'cwd raft_id run_number'.split())

class EOAcqConfig(dict):
    """
    Read the entries as key/value pairs from the acquisition
    configuration file that specifies the frames, exposure times, and
    signal levels for the various electro-optical tests.
    """
    def __init__(self, acq_config_file):
        """
        Parameters
        ----------
        acq_config_file : str
            The path to the acquisition configuration file.
        """
        super(EOAcqConfig, self).__init__()
        with open(acq_config_file) as input_:
            for line in input_:
                tokens = line.split()
                if len(tokens) < 2:
                    continue
                key = tokens[0].upper()
                if not self.has_key(key):
                    self[key] = tokens[1]

    def get(self, key, default="NOT FOUND"):
        """
        Get the desired value for the specified key, providing an
        optional default.
        """
        return super(EOAcqConfig, self).get(key, default)

class EOAcquisition(object):
    """
    Base class for TS8 electro-optical data acquisition.
    """
    def __init__(self, seqfile, acq_config_file, acqname, metadata,
                 subsystems, ccd_names, logger=logger, slit_id=2):
        """
        Parameters
        ----------
        seqfile : str
            The name of the sequencer file.
        acq_config_file : str
            The name of the acquisition configuration file.
        acqname : str
            The test type, e.g., 'FE55', 'FLAT', 'SFLAT', etc..
        metadata : namedtuple
            A nametuple of test-wide metadata, specifically, the
            current working directory, the LSST unit ID for the raft,
            and the run number.
        subsystems : dict
            A dictionary of CCS subsystems, keyed by standard attribute
            names for the CcsSubsystems class, i.e., 'ts', 'ts8', 'pd',
            and 'mono'.  If None, then the default subsystems, 'ts', 'ts8',
            'ts/PhotoDiode', and 'ts/Monochromator', will be attached.
        ccd_names : dict
            Dictionary of namedtuple containing the CCD .sensor_id and
            .maufacturer_sn information, keyed by slot name.
        logger : logging.Logger
            Log commands using the logger.info(...) function.
        slit_id: int [2]
            ID of the monochormator slit to set via ._set_slitwidth(...)
        """
        if subsystems is None:
            subsystems = dict(ts8='cr-raft', pd='ts8-bench/Monitor',
                              mono='ts8-bench/Monochromator')
        print("subsystems = ",subsystems)
        self.sub = CcsSubsystems(subsystems=subsystems, logger=logger)
        self.sub.write_versions(os.path.join(metadata.cwd, 'ccs_versions.txt'))
        self._check_subsystems()

# The following shouldn't be needed ... still investigating why
        self.sub.ts8 = CCS.attachSubsystem('cr-raft')
        self.sub.pd = CCS.attachSubsystem('ts8-bench/Monitor')
        self.sub.mono = CCS.attachSubsystem('ts8-bench/Monochromator')

        write_REB_info(self.sub.ts8,
                       outfile=os.path.join(metadata.cwd, 'reb_info.txt'))
        set_ccd_info(self.sub, ccd_names, logger)
        self.sub.ts8.sendSynchCommand('setDefaultImageDirectory %s/S${sensorLoc}'
                                  % metadata.cwd)
        self.seqfile = seqfile
        self.eo_config = EOAcqConfig(acq_config_file)
        self.acqname = acqname
        self.md = metadata
        self.logger = logger
        self.slit_id = slit_id
        self._set_ts8_metadata()
        self._get_exptime_limits()
        self._get_image_counts()
        self._set_default_wavelength()
        self.current_slitwidth \
            = int(self.eo_config.get('DEFAULT_SLITWIDTH', default=240))
        self.set_slitwidth(self.current_slitwidth, self.slit_id)
        self._read_instructions(acq_config_file)
#        self._fn_pattern = "CR_${CCDSerialLSST}_${testType}_${imageType}_${SequenceInfo}_${RunNumber}_${timestamp}.fits"
#        self._fn_pattern = "${CCDSerialLSST}_${testType}_${imageType}_${SequenceInfo}_${RunNumber}_${timestamp}.fits"
#        self._fn_pattern = "${CCDSerialLSST}_${testType}_${imageType}_${SequenceInfo}_${RunNumber}_${timestamp}.fits"
        self._fn_pattern = "${rebName}${sensorId}_${testType}_${imageType}_${RunNumber}_${timestamp}.fits"
#        print("****** Would have loaded sequencer %s \nbut Homer told me not to until checking with Sven. !!!!!")
        self.sub.ts8.sendSynchCommand("loadSequencer", self.seqfile)
        self.sub.mono.sendSynchCommand("openShutter")

    def _check_subsystems(self):
        """
        Check that the required subsystems are present.
        """
        required = 'mono pd'.split()
        missing = []
        for subsystem in required:
            if not hasattr(self.sub, subsystem):
                missing.append(subsystem)
        if missing:
            raise RuntimeError("EOAcquisition: missing CCS subsystems:"
                               + '\n'.join(missing))

    def _set_ts8_metadata(self):
        """
        Pass metadata such as image output directory, raft name, run
        number to the ts8 subsystem.
        """
        command = "setDefaultImageDirectory %s/S${sensorLoc}" % self.md.cwd
        self.sub.ts8.sendSynchCommand(command)
        command = "setPrimaryHeaderKeyword RaftName %s" % self.md.raft_id
        self.sub.ts8.sendSynchCommand(command)
        command = "setPrimaryHeaderKeyword RunNumber %s" % self.md.run_number
        self.sub.ts8.sendSynchCommand(command)
        print("temp = ",self.sub.ts8.sendSynchCommand("getChannelValue WREB.CCDtemp0"))
#        self.sub.ts8.sendSynchCommand("setPrimaryHeaderKeyword","CRSACCDTemp",float(self.sub.ts8.sendSynchCommand("getChannelValue WREB.CCDtemp0")))
#        print("setting CCDTEMP using ","setPrimaryHeaderKeyword","CRSACCDTemp",float(self.sub.ts8.sendSynchCommand("getChannelValue WREB.CCDtemp0")))
        self.sub.ts8.sendSynchCommand("setPrimaryHeaderKeyword","MeasuredTemperature",float(self.sub.ts8.sendSynchCommand("getChannelValue WREB.CCDtemp0")))
        print("setting CCDTEMP using ","setPrimaryHeaderKeyword","MeasuredTemperature",float(self.sub.ts8.sendSynchCommand("getChannelValue WREB.CCDtemp0")))

    def _get_exptime_limits(self):
        """
        Get the minimum and maximum exposure times from the config file.
        """
        self.exptime_min = float(self.eo_config.get('%s_LOLIM' % self.acqname,
                                                    default='0.025'))
        self.exptime_max = float(self.eo_config.get('%s_HILIM' % self.acqname,
                                                    default='600.0'))

    def _get_image_counts(self):
        """
        Get the number of exposures and bias frames to take for each
        acquisition instruction.
        """
        self.imcount = int(self.eo_config.get('%s_IMCOUNT' % self.acqname,
                                              default='1'))
        self.bias_count = int(self.eo_config.get('%s_BCOUNT' % self.acqname,
                                                 default='1'))

    def _set_default_wavelength(self):
        """
        Set the default wavelength for all acquistions.
        """
        self.wl = float(self.eo_config.get('%s_WL' % self.acqname,
                                           default="550.0"))
        self.set_wavelength(self.wl)

    def _set_slitwidth(self, tokens, index):
        slit_width_changed = False
        try:
            width = int(tokens[index])
        except IndexError:
            width = int(self.eo_config.get('DEFAULT_SLITWIDTH', default=240))
        if width != self.current_slitwidth:
            self.set_slitwidth(width, self.slit_id)
            self.current_slitwidth = width
            slit_width_changed = True
        return slit_width_changed

    def set_slitwidth(self, width, slit_id):
        """Set the monochromator slit width."""
        self.sub.mono.sendSynchCommand('setSlitSize', slit_id, width)

    def set_wavelength(self, wl):
        """
        Set the monochromator wavelength.

        Parameters
        ----------
        wl : float
            The desired wavelength in nm.
        """
#        command = "setTimeout 5000"
#        rwl = self.sub.mono.sendSynchCommand(command)

        command = "setWaveAndFilter %s" % wl
        rwl = self.sub.mono.sendSynchCommand(Duration.ofSeconds(10),command)

        self.sub.ts8.sendSynchCommand("setPrimaryHeaderKeyword MonochromatorWavelength %s" % rwl)
        return rwl

    def _read_instructions(self, acq_config_file):
        """
        Read the instructions for the current test type from the
        acquisition configuration file.
        """
        self.instructions = []
        with open(acq_config_file) as input_:
            for line in input_:
                tokens = line.split()
                if tokens and tokens[0] == self.acqname.lower():
                    self.instructions.append(tokens)

    def run(self):
        """
        Default run method to be re-implemented in subclasses.
        """
        raise NotImplementedError("Subclass must implement this function")

    @property
    def test_type(self):
        """
        The test type, e.g., 'FLAT', 'FE55', 'SFLAT', 'DARK', etc..
        """
        return self.acqname.upper()

    def take_image(self, seqno, exptime, openShutter, actuateXed,
                   image_type, test_type=None, file_template=None,
                   timeout=500, max_tries=3, try_wait=10.):
        """
        Take an image.

        Parameters
        ----------
        seqno : int
            The sequence number to be written into the FITS file name.
        exptime : float
            The exposure time in seconds.
        openShutter : bool
            Flag to indicate that the monochromator shutter should be
            opened for the exposure.
        actuateXed : bool
            Flag to indicate that the XED arms should be deployed so
            that a Fe55 exposure can be taken.
        image_type : str
            The image type for writing to the FITS header and filename.
            It must be one of "FLAT", "FE55", "DARK", "BIAS", "PPUMP".
        test_type : str, optional
            The test type to be written in to the FITS header and filename.
            If None, then the value set in the constructor is used.  This
            override option is needed since the superflat commands in the
            acq config file are labeled by 'SFLAT', whereas the FITS info
            needs to encode the wavelength of exposure, e.g., 'SFLAT_500'.
        file_template : str, optional
            The file template used by the CCS code for writing FITS
            filenames.  FLAT, SFLAT, and QE acquistions require special
            templates; all other acquisitions can use the default.
        timeout : int, optional
            Timeout (in seconds) for the synchronous "acquireExposureMaster"
            commmand.  Default: 500.
        max_tries : int, optional
            The number of maximum number of tries for the
            "acquireExposureMaster" command.  Default: 3.  If the command
            does not succeed in max_tries, the exception from the CCS code
            is re-raised.
        try_wait : float, optional
            The number of seconds to wait between subsequent tries of
            the "acquireExposureMaster" command.  Default: 10.

        Returns
        -------
        Result object from the CCS synchCommand(timeout, "acquireExposureMaster")
        execution.
        """
        if test_type is None:
            test_type = self.test_type
        if file_template is None :
            file_template = self._fn_pattern
        elif len(file_template) is 0 : 
            file_template = self._fn_pattern
        print("len(file_template) = ",len(file_template))

        self.logger.info("%s: taking image type %s %d", test_type, image_type,
                         seqno)
        self.logger.info("file_template = %s , fn_pattern = %s", file_template, self._fn_pattern)
        self.sub.ts8.sendSynchCommand("setPrimaryHeaderKeyword TestType %s" % test_type)
        self.sub.ts8.sendSynchCommand("setPrimaryHeaderKeyword ImageType %s" % image_type)
        self.sub.ts8.sendSynchCommand("setPrimaryHeaderKeyword SeqInfo %s" % seqno)

#hn        self.verify_sequencer_params()
#hn        self.ccd_clear(1)

#        command = 'acquireExposure %d %s %s \"%s\"' \
#            % (1000*exptime, openShutter, actuateXed, file_template)
#        command = 'acquireExposureMaster %d %s %s \"%s\"' \
#            % (1000*exptime, openShutter, actuateXed, file_template)
        # ensure timeout exceeds exposure time by 20 seconds.
        timeout = Duration.ofSeconds(int(max(timeout, exptime + 20)))
        for itry in range(max_tries):
            try:
#                result = self.sub.ts8.sendSynchCommand(timeout,command)
#                result = self.sub.ts8.synchCommand(timeout, command)
                result = acquireExposureMaster(1000*exptime, openShutter, actuateXed, "%s/S${sensorLoc}" % self.md.cwd, file_template)
                return result
            except (StandardError, java.lang.Exception) as eobj:
                self.logger.info("EOAcquisition.take_image: try %i failed",
                                 itry)
                self.logger.info(str(eobj))
                time.sleep(try_wait)
        raise RuntimeError("Failed to take an image after %i tries."
                           % max_tries)

    def image_clears(self, nclears=0, exptime=5):
        """
        Take some bias frames to clear the CCDs.

        nclears : int, optional
            The number of bias images to take.  Default: 2.
        exptime : float, optional
            Exposure time in seconds. Default: 5.
        """
        for i in range(nclears):
            try:
                self.take_image(0, exptime, False, False, "biasclear",
                                file_template='')
            except StandardError as eobj:
                self.logger.info("Clear attempt %d failed:\n %s", i, str(eobj))
                time.sleep(1.0)

    def bias_image(self, seqno, max_tries=3):
        """
        Take bias images.
        """
        exptime = 0
        openShutter = False
        actuateXed = False
        self.take_image(seqno, exptime, openShutter, actuateXed, "BIAS",
                        timeout=150, max_tries=max_tries)

    def dark_image(self, seqno, exptime, max_tries=3):
        """
        Take dark image
        """
        openShutter = False
        actuateXed = False
        timeout = int(max(150, exptime + 20))
        self.take_image(seqno, exptime, openShutter, actuateXed, "DARK",
                        timeout=timeout, max_tries=max_tries)

    def measured_flux(self, wl, seqno=0, fluxcal_time=2.):
        """
        Compute the measured flux by taking an exposure at the
        specified wavelength.

        Parameters
        ----------
        wl : float
            The wavelength in nm.
        seqno : int, optional
            The sequence number for the exposure.  Default: 0.
        fluxcal_time : float, optional
            The exposure time in seconds for the flux calibration exposure.
            Default: 2.

        Returns
        -------
        float :
            The flux value in e-/pixel/s.
        """
        self.set_wavelength(wl)
        openShutter = True
        actuateXed = False
        # Take a test image.
        self.take_image(seqno, fluxcal_time, openShutter, actuateXed,
                        "prefluxcalib", file_template='')
        # The calibration image.
        fits_files = self.take_image(seqno, fluxcal_time, openShutter,
                                     actuateXed, "fluxcalib", max_tries=3)
        flux_sum = 0.
        if isinstance(fits_files, int):
            # We must be using a subsystem-proxy the ts8 subsystem.
            # TODO: Find a better way to handle the subsystem-proxy
            # case.
            return 1
        for fits_file in fits_files:
            print("fits_file = ",fits_file)
            print("self.md.cwd = ",self.md.cwd)
            file_path = glob.glob(os.path.join(self.md.cwd, '*', fits_file))[0]
            print('file_path = %s' % file_path)
#            print('export = ',os.popen('printenv').readline())
#            print('CRJOBSDIR = ',os.getenv('CRJOBSDIR'))
            crjd = '/home/homer/cr/jh_inst/1.0.1/CR-jobs-1.0.1/python'
            pydir = '/gpfs/slac/lsst/fs2/u1/dh/software/centos7-gcc48/stack/v16_py3/python/miniconda3-4.3.21/bin/'
#            cmndstr = '%s/python %s/get_signal_level.py %s 2>&1' % (pydir,crjd,file_path)
            cmndstr = 'bash -c "source /home/homer/cr/setup.sh 2>&1 ; %s/get_signal_level.py %s 2>&1"' % (crjd,file_path)
#            cmndstr = 'which python'
            print("cmndstr = ",cmndstr)
#            os.system(cmndstr)
            print("============================")
#            sigstr = os.popen(cmndstr, shell=True).readline()
            my_env = os.environ.copy()
#my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
#      subprocess.Popen(my_command, env=my_env)
            p = subprocess.Popen(cmndstr, shell=True, bufsize=0, stdout=subprocess.PIPE, universal_newlines=True, env=my_env)
            p.wait()
            sigstr = p.stdout.read()
            p.stdout.close()
#            sigstr = subprocess.check_output('%s/get_signal_level.py' % (crjd),'%s' % (file_path))
            print('sigstr = ',sigstr)
            avg = float(sigstr)

            avg = max(avg,999.)
            print("average signal = ",avg)

#ts8            command = "getFluxStats %s" % file_path
#ts8            flux_sum += \
#ts8                float(self.sub.ts8.sendSynchCommand(command))
            flux_sum += avg
        return flux_sum/len(fits_files)

    def compute_exptime(self, target_counts, meas_flux):
        """
        Compute the exposure time for a specified wavelength and
        target signal level.

        Parameters
        ----------
        target_counts : float
            The desired signal level in e-/pixel.
        meas_flux : float
            The incident flux (at the current wavelength setting) in
            e-/pixel/s.

        Returns
        -------
        float :
            The exposure time in seconds.
        """
        exptime = target_counts/meas_flux
        exptime = min(max(exptime, self.exptime_min), self.exptime_max)
        return exptime

    def getParallelHighConfig(self):
        """
        get phi0, phi1, phi2 existing values of pclkHighP
        """
        command = "printConfigurableParameters"
        res = str(self.sub.ts8dac0.sendSynchCommand(command))
        m = re.search(r"pclkHighP: ([-\d]+\.\d+),", res)
        if not m:
            self.logger.info("m is None, res=%s", res)
            return None
        phi0 = float(m.group(1))
        if phi0 < 1.0:
            self.logger.info("ts8dac0.pclkHighP=%s < 1.0", phi0)
            return None
        res = str(self.sub.ts8dac1.sendSynchCommand(command))
        m = re.search(r"pclkHighP: ([-\d]+\.\d+),", res)
        if not m:
            self.logger.info("m is None, res=%s", res)
            return None
        phi1 = float(m.group(1))
        if phi1 < 1.0:
            self.logger.info("ts8dac1.pclkHighP=%s < 1.0", phi1)
            return None
        res = str(self.sub.ts8dac2.sendSynchCommand(command))
        m = re.search(r"pclkHighP: ([-\d]+\.\d+),", res)
        if not m:
            self.logger.info("m is None, res=%s", res)
            return None
        phi2 = float(m.group(1))
        if phi2 < 1.0:
            self.logger.info("ts8dac2.pclkHighP=%s < 1.0", phi2)
            return None
        return phi0, phi1, phi2

    def getParallelLowConfig(self):
        """
        get plo0, plo1, plo2 existing values of pclkLowP
        """
        command = "printConfigurableParameters"
        res = str(self.sub.ts8dac0.sendSynchCommand(command))
        m = re.search(r"pclkLowP: ([-\d]+\.\d+),", res)
        if not m:
            self.logger.info("m is None, res=%s", res)
            return None
        plo0 = float(m.group(1))
        if plo0 > 0.5:
            self.logger.info("ts8dac0.pclkLowP: %s > 0.5", plo0)
            return None
        res = str(self.sub.ts8dac1.sendSynchCommand(command))
        m = re.search(r"pclkLowP: ([-\d]+\.\d+),", res)
        if not m:
            self.logger.info("m is None, res=%s", res)
            return None
        plo1 = float(m.group(1))
        if plo1 > 0.5:
            self.logger.info("ts8dac1.pclkLowP: %s > 0.5", plo1)
            return None
        res = str(self.sub.ts8dac2.sendSynchCommand(command))
        m = re.search(r"pclkLowP: ([-\d]+\.\d+),", res)
        if not m:
            self.logger.info("m is None, res=%s", res)
            return None
        plo2 = float(m.group(1))
        if plo2 > 0.5:
            self.logger.info("ts8dac2.pclkLowP: %s > 0.5", plo2)
            return None
        return (plo0, plo1, plo2)

    def get_ccdtype(self):
        """ return ccdtype as a string"""
        res = str(self.sub.ts8.sendSynchCommand("getCcdType"))
        if re.match(r"^e2v$", res):
            return "e2v"
        elif re.match(r"^itl$", res):
            return "itl"
        else:
            self.logger.info("CCD Type unknown, returning None")
            return None

    def verify_sequencer_params(self):
        """ Check that CleaningNumber = 0 and ClearCount = 1
        Otherwise the wrong sequencer is loaded
        """
        #- CleaningNummber = [0, 0, 0]
        res = str(self.sub.ts8.sendSynchCommand(
                         "getSequencerParameter", "CleaningNumber"))
        if not re.match(r"\[0, 0, 0\]", res):
            self.logger.info("SeqParam CleaningNumber:%s invalid", res)
            raise java.lang.Exception("Bad Sequencer: CleaningNumber=0 required")
        #- ClearCount = [1, 1, 1]
        res = str(self.sub.ts8.sendSynchCommand(
                             "getSequencerParameter", "ClearCount"))
        if not re.match(r"\[1, 1, 1\]", res):
            self.logger.info("SeqParam ClearCount:%s invalid", res)
            raise java.lang.Exception("Bad Sequencer: ClearCount=1 required")

    def ccd_clear(self, nclears):
        """
        clear the ccd according to type and conditions
        ccdtype==itl: just run clear main as is
        ccdtype==e2v: if running unipolar mode do shifted clearing
        where shifted clear drops/raises P-High before/after clearing
        and where the shifted value "phi_shifted" is hardcoded below
        """
        if nclears < 1:
            return
        ccdtype = self.get_ccdtype()
#        if ccdtype == 'e2v':
#            phi_shifted = 5.5  #- hard coded value for now
#            #- verify input value makes sense
#            #
#            if phi_shifted < 5.0 or phi_shifted > 7.0:
#                self.logger.info("P-HI:%s not in range 5.0..7.0", phi_shifted)
#                raise java.lang.Exception("Bad phi_shifted value {}".format(phi_shifted))
#            #
#            #- get original values for Parallel high and low rails
#            #
#            phi = self.getParallelHighConfig()
#            if phi is None:
#                self.logger.info("getParallelHighConfig() = None")
#                #- throw an exception here or something
#                raise java.lang.Exception("failed getting PHi config")
#            #
#            plo = self.getParallelLowConfig()
#            if plo is None:
#                self.logger.info("getParallelLowConfig() = None")
#                #- throw an exception here or something
#                raise java.lang.Exception("failed getting PLow config")
#            #
#            #- determine operating mode (unipolar (3) or bipolar (0))
#            #
#            self.logger.info("phi[]= %s", phi)
#            self.logger.info("plo[]= %s", plo)
#            cnt = 0
#            for i in range(len(phi)):
#                if phi[i] > 7.5 and plo[i] >= 0.0  and plo[i] < 2.0:
#                    cnt += 1
#                if phi[i] > 2.0 and phi[i] < 7.0  and plo[i] < -3.0:
#                    cnt -= 1
#            if cnt == 3:
#                unipolar = True
#                self.logger.info("Parallel Voltages are unipolar => Shifted Clearing")
#            elif cnt == -3:
#                unipolar = False
#                self.logger.info("Parallel Voltages are bipolar => Regular Clearing")
#            else:
#                raise java.lang.Exception(
#                    "invalid mode: must be bipolar (+/-) or unipolar (>0)")
#            if unipolar:
#                #
#                #- change to the new value
#                #
#                self.logger.info("changing dac %s to %s...",
#                                 "pclkHighP", phi_shifted)
#                self.sub.ts8dac0.sendSynchCommand("change", "pclkHighP", phi_shifted)
#                self.sub.ts8dac1.sendSynchCommand("change", "pclkHighP", phi_shifted)
#                self.sub.ts8dac2.sendSynchCommand("change", "pclkHighP", phi_shifted)
#                self.sub.ts8.sendSynchCommand("loadDacs true")
#                #
#        #- Perform the Clear main
#        #
        self.logger.info("Clearing CCD %s times...", nclears)
        for _ in range(nclears):
            self.sub.ts8.sendSynchCommand("setSequencerStart", "Clear")
            self.sub.ts8.sendSynchCommand("startSequencer")
            self.sub.ts8.sendSynchCommand("waitSequencerDone", 1000)
            self.sub.ts8.sendSynchCommand("setSequencerStart", "Bias")
#        if ccdtype == 'e2v':
#            if unipolar:
#                #
#                #- change back to original value
#                #
#                self.logger.info("changing dac %s to %s...",
#                                 "pclkHighP", phi)
#                self.sub.ts8dac0.sendSynchCommand("change", "pclkHighP", phi[0])
#                self.sub.ts8dac1.sendSynchCommand("change", "pclkHighP", phi[1])
#                self.sub.ts8dac2.sendSynchCommand("change", "pclkHighP", phi[2])
#                self.sub.ts8.sendSynchCommand("loadDacs true")
#                #

class PhotodiodeReadout(object):
    """
    Class to handle monitoring photodiode readout.
    """
    def __init__(self, exptime, eo_acq_object, max_reads=2048):
        """
        Parameters
        ----------
        exptime : float
            Exposure time in seconds for the frame to be taken.
        eo_acq_object : EOAcquisition object
            An instance of a subclass of EOAcquisition.
        max_reads : int, optional
            Maximum number of reads of monitoring photodiode.  Default: 2048.
        """
        self.sub = eo_acq_object.sub
        self.md = eo_acq_object.md
        self.logger = eo_acq_object.logger
        self._exptime = exptime
        self._buffertime = 2.0

        # for exposures over 0.5 sec, nominal PD readout at 60Hz,
        # otherwise 240Hz
        if exptime > 0.5:
            nplc = 1.
        else:
            nplc = 0.25

        # add a buffer to duration of PD readout
        nreads = min((exptime + self._buffertime)*60./nplc, max_reads)
        self.nreads = int(nreads)

        # adjust PD readout when max_reads is reached
        # (needs to be between 0.001 and 60 - add code to check)
        self.nplc = (exptime + self._buffertime)*60./nreads
        self._pd_result = None
        self._start_time = None

    def start_accumulation(self):
        """
        Start the asynchronous accumulation of photodiode current readings.
        """

        # get Keithley picoAmmeters ready by resetting and clearing buffer
        self.sub.pd.sendSynchCommand("reset")
        self.sub.pd.sendSynchCommand("clrbuff")
        self.sub.pd.sendSynchCommand("setCurrentRange 0.0000002")

        # start accummulating current readings
        self._pd_result = self.sub.pd.sendAsynchCommand("accumBuffer", self.nreads,
                                                    self.nplc, True)
        self._start_time = time.time()
        self.logger.info("Photodiode readout accumulation started at %f",
                         self._start_time)

        running = False
        while not running:
            try:
                running = self.sub.pd.sendSynchCommand("isAccumInProgress")
            except StandardError as eobj:
                self.logger.info("PhotodiodeReadout.start_accumulation:")
                self.logger.info(str(eobj))
            self.logger.info("Photodiode checking that accumulation started at %f",
                         time.time() - self._start_time)
            time.sleep(0.25)

    def write_readings(self, fits_files, seqno, icount=1):
        """
        Output the accumulated photodiode readings to a text file.
        """
        # make sure Photodiode readout has had enough time to run
        pd_filename = os.path.join(self.md.cwd,
                                   "pd-values_%d-for-seq-%d-exp-%d.txt"
                                   % (int(self._start_time), seqno, icount))
        self.logger.info("Photodiode about to be readout at %f",
                         time.time() - self._start_time)

        result = self.sub.pd.sendSynchCommand("setTimeout 1000")
        result = self.sub.pd.sendSynchCommand(Duration.ofSeconds(1000),"readBuffer %s" % pd_filename)
        print("pd_filename = ",pd_filename)
        self.logger.info("Photodiode readout accumulation finished at %f, %s",
                         time.time() - self._start_time, result)

        for fits_file in fits_files:
            full_path = glob.glob('%s/*/%s' % (self.md.cwd, fits_file))[0]
            noextpath = full_path.split('.fits')[0]
            co_pd_file = noextpath + "_pdvals.txt"
            os.popen('cp -p %s %s' % (pd_filename,co_pd_file))

        return pd_filename

    def add_pd_time_history(self, fits_files, pd_filename):
        "Add the photodiode time history as an extension to the FITS files."
        for fits_file in fits_files:
            full_path = glob.glob('%s/*/%s' % (self.md.cwd, fits_file))[0]
            command = "addBinaryTable %s %s AMP0.MEAS_TIMES AMP0_MEAS_TIMES AMP0_A_CURRENT %d" % (pd_filename, full_path, self._start_time)
            self.sub.ts8.sendSynchCommand(command)
            self.logger.info("Photodiode readout added to fits file %s",
                             fits_file)

    def get_readings(self, fits_files, seqno, icount):
        """
        Output the accumulated photodiode readings to a text file and
        write that time history to the FITS files as a binary table
        extension.
        """
        pd_filename = self.write_readings(fits_files,seqno, icount)
#        try:
#            self.add_pd_time_history(fits_files, pd_filename)
#        except TypeError:
#            # We must be using a subsystem-proxy for the ts8
#            # subsystem.  TODO: Find a better way to handle the
#            # subsystem-proxy case.
#            pass

from SNMPLib import SNMPLib
import config
import time
import logging

loggerlocal = logging.getLogger('framework.log')

snmpobj = SNMPLib()

class MSConfig:

    def __init__(self):
        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']

    def checkmscores(self):

        audiocores = snmpobj.getMSaudiocores()
        loggerlocal.debug("Checking the MS cores")
        if audiocores == '0':
            print "There are no audio cores, Setting default core (equal audio & video)"
            allocated = int(snmpobj.snmpget('caNumMpCores.0'))
            if allocated >= 4:
                snmpobj.snmpset('caNumVxmlCores.0', '0', 'u')
                snmpobj.snmpset('caNumHdEncCores.0', '0', 'u')
                snmpobj.snmpset('caNumVideoCores.0', str(allocated/2), 'u')
            else:
                print "SUT has less than 4 cores"
                logging.debug("SUT is having less than 4 MP cores. ")
        else:
            print "SUT has " + audiocores + "cores... "

    # Load should be running during
    def refactorcores(self, achievedports='1000', videoload = False, confload = False):

        loggerlocal.debug("Evaluating whether core refactoring is necessary based on the achieved ports %s" \
                          %(achievedports))
        if int(achievedports) > 1000:
            loggerlocal.debug("Achieved ports are more thank 1000, core refactoring is in progress... ")
            print "Number of achieved ports are more than 1000, refactoring SUT cores"
            # Getting the SUT cores
            audiocores = snmpobj.getMSaudiocores()
            videocores = snmpobj.snmpget('caNumVideoCores.0')
            #hcvideocores = snmpobj.snmpget('caNumHdEncCores.0')

            # Getting the DSP Utilization
            '''
            audiodsp = snmpobj.snmpget('dspstatMaxAudioDspUtilizationModeled.2')
            videodsp = snmpobj.snmpget('dspstatMaxVideoDspUtilizationModeled.2')
            hdvideodsp = snmpobj.snmpget('dspstatMaxHcVideoDspUtilizationModeled.2')
            '''

            if not videoload and not confload:
                newaudiocore = str(int((round((1000/int(achievedports)) * int(audiocores), 0))))
                snmpobj.snmpset('caNumVideoCores.0', int(videocores)+(int(audiocores)-int(newaudiocore)), 'u')
            else:
                pass
            loggerlocal.debug("Core refactoring is completed")
            return True

        else:
            return False

    def setsyslog(self):
        loggerlocal.debug(" Setting SCRM severity to - Notice and others to - Warning")
        snmpobj.snmpset('syslogConProtSeverity.1', '16', 'u')
        snmpobj.snmpset('syslogSESeverity.1', '16', 'u')
        snmpobj.snmpset('syslogOAMPSeverity.1', '16', 'u')
        snmpobj.snmpset('syslogPlatformSeverity.1', '16', 'u')
        snmpobj.snmpset('syslogMSMLSeverity.1', '16', 'u')
        snmpobj.snmpset('syslogMpSeverity.1', '16', 'u')
        snmpobj.snmpset('syslogSpeechManagerSeverity.1', '16', 'u')
        snmpobj.snmpset('syslogSCRMSeverity.1', '32', 'u') # Setting SCRM to Notice

    def sutresetservice(self):
        loggerlocal.debug("Making SUT OOS ")
        snmpobj.snmpset('comSetServiceMode.1.2', '0', 'i')
        time.sleep(3)
        snmpobj.snmpset('comSetServiceMode.1.2', '1', 'i')
        time.sleep(5)
        if snmpobj.checksnmpresult('1'):
            loggerlocal.debug("SUT is InService")
        else:
            loggerlocal.debug("SUT is still OSS, Please check ")

    # nodeReboot.0

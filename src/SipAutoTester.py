#!/usr/bin/python
import pexpect
import os
import sys
import time
import config
import logging
from SNMPLib import SNMPLib
import CapacityDet
import commands

snmpobj = SNMPLib()


class SipAutoTester:

    def __init__(self, logpath):
        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']
        self.rtpgIp = config.rtpgCredentials['rtpgIp']
        self.loadDur = config.loadDurationDetails['loadduration']
        self.SATPath = config.SATDetails['SATPath']
        self.logPath = logpath
        self.logger = logging.getLogger("ClearMrfLog.py")
        self.logger.debug("clearing MRF Log ")
        self.loadAT = config.loadDetails['ATFile']
        self.loadATmodel = config.loadDetails['modelCfg']
        self.sutctrlip = config.swMrfCredentials['MS_Server_Control_IP']

    def prepareATcfg(self):

        print "Replacing SipMSIPAddress & SipMSIPAddressSCC values "
        commands.getoutput("sed -i '/SipMSIPAddress/d' %s/%s" %(self.SATPath, self.loadAT))
        commands.getoutput('sed -i "\$aSipMSIPAddress=%s" %s/%s'%(self.sutctrlip, self.SATPath, self.loadAT))
        commands.getoutput('sed -i "\$aSipMSIPAddressSCC=%s" %s/%s'%(self.mrfIp, self.SATPath, self.loadAT))


    def startSAT(self):
        os.system('cp /tmp/config.py  .')
        os.system('rm -rf %sat*' %(self.SATPath))
        os.system('cp %sMscConfig.cfg .' %(self.SATPath))
        time.sleep(10)
        os.system('cp %s%s %s/models.standard/' %(self.SATPath, self.loadATmodel, self.SATPath))
        child=pexpect.spawn('%sSipAutoTester_Rel_0403 -c %s%s' %(self.SATPath, self.SATPath, self.loadAT))
        child.timeout = float(self.loadDur)
        first = child.expect(['0 : %s' %(self.rtpgIp)])
        child.logfile = sys.stdout
        child_before = child.before
        print child_before
        child_after = child.after
        print child_after
        if first == 0:
            child.sendline('10')
            next_menu = child.expect(["Append '-'"])
            if next_menu == 0:
                child.sendline('1050')
                try:
                    exit = child.expect('Anything', timeout=180)
                except pexpect.TIMEOUT:
                    print "value :"

                maxAudioModel = snmpobj.snmpget('dspstatMaxAudioDspUtilizationModeled.2')
                print "The MAX Audio Util in SUT is " + maxAudioModel + " %"

                if int(maxAudioModel) <= 65:
                    # time.sleep(float(self.loadDur))
                    print "I'm here mukesh"
                    child.timeout = 600
                    child.sendline('5')
                    quit = child.expect("selection", timeout=1200)
                    child.sendline('0')
                    final_quit = child.expect("Entered")
                    child.sendline('Y')
                    CapacityDetobj = CapacityDet.CapacityDet(maxAudioModel)
                    CapacityDetobj.Dynamiccheck()
                    return False
                elif int(maxAudioModel) > 75:
                    print "DSP's % are more than 80, so need to decreasing the ports"
                    child.sendline('5')
                    quit = child.expect("selection", timeout=1200)
                    child.sendline('0')
                    final_quit = child.expect("Entered")
                    child.sendline('Y')
                    CapacityDetobj = CapacityDet.CapacityDet(maxAudioModel)
                    CapacityDetobj.decreaseThePorts()
                    return False
                else:
                    # child.timeout=float(self.loadDur)
                    print "inside 8 hour load"
                    child.timeout = float(self.loadDur)
                    child.sendline(' ')
                    try:
                        exit = child.expect('Anything')
                    except pexpect.TIMEOUT:
                        print "value :"
                    print "I'm here mike"
                    child.sendline('5')
                    quit = child.expect('selection', timeout=1200)
                    child.sendline('0')
                    final_quit = child.expect("Entered")
                    child.sendline('Y')
                    print "Load Model ended. @ The End"
                    return True

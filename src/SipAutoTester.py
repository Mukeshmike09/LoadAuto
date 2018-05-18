#!/usr/bin/python
import pexpect
import os
import sys
import time
import config
import logging
import re


class SipAutoTester:

    def __init__(self,logpath):
        self.mrfIp=config.swMrfCredentials['mrfIp']
        self.mrfUserName=config.swMrfCredentials['mrfUserName']
        self.mrfPassword=config.swMrfCredentials['mrfPassword']
        self.rtpgIp=config.rtpgCredentials['rtpgIp']
        self.loadDur=config.loadDurationDetails['loadduration']
        self.SATPath=config.SATDetails['SATPath']
        self.logPath=logpath
        self.logger = logging.getLogger("ClearMrfLog.py")
        self.logger.debug("clearing MRF Log ")
        self.loadAT=config.loadDetails['ATFile']
        self.loadATmodel=config.loadDetails['modelCfg']

    def startSAT(self):
        os.system('cp /tmp/config.py  .')
        os.system('rm -rf %sat*'%(self.SATPath))
        os.system('cp %sMscConfig.cfg .'%(self.SATPath))
        time.sleep(10)
        os.system('cp %s%s %s/models.standard/'%(self.SATPath,self.loadATmodel,self.SATPath))
        child=pexpect.spawn('%sSipAutoTester_Rel_0403 -c %s%s'%(self.SATPath,self.SATPath,self.loadAT))
        child.timeout=float(self.loadDur)
        first = child.expect(['0 : %s'%(self.rtpgIp)])
        child.logfile = sys.stdout
        out = child.before
        print out
        #self.logger.console("%s"%(out))
        next = child.after
        #self.logger.console("%s"%(next))
        print next
        if(first == 0):
            child.sendline('10')
            next_menu = child.expect(["Append '-'"])
        if next_menu == 0:
            child.sendline('1050')
            time.sleep(120)
            k, number = commands.getstatusoutput(
                'snmpget -v2c -Ovq -m /root/.snmp/mibs/MS.my %s dspstatMaxAudioDspUtilizationModeled.2' % (self.mrfIp))
            print "k,mike=commands.getstatusoutput('snmpget -v2c -Ovq -m /root/.snmp/mibs/MS.my %s dspstatMaxAudioDspUtilizationModeled.2'%(self.mrfIp))"
            # number=os.system('snmpget -v2c -Ovq -m /root/.snmp/mibs/MS.my 10.201.4.179 dspstatMaxAudioDspUtilizationModeled.2')
            if number <= 65 and number <= 75:
                # time.sleep(float(self.loadDur))
                child.sendline('5')
                quit = child.expect("selection")
                child.sendline('0')
                final_quit = child.expect("Entered")
                child.sendline('Y')
                CapacityDetobj = CapacityDet.CapacityDet(number)
                CapacityDetobj.Dynamiccheck()
            else:
                # child.timeout=float(self.loadDur)
                child.timeout = 600
                child.sendline('5')
                quit = child.expect("selection")
                child.sendline('0')
                final_quit = child.expect("Entered")
                child.sendline('Y')

#            	os.system("cp %sat* %s"%(self.SATPath,self.logPath))
#obj=SipAutoTester()		
#obj.startSAT()
#obj.copySatLog()


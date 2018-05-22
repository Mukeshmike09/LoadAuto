#!/usr/bin/python
import logging
import healthCheck
import sys
import time
import threading
import SipAutoTester
import os
import ClearMrfLog
import pexpect
import topProcess
import config

from MSConfig import MSConfig

objMSConfig = MSConfig()

class mainProgram:

    def __init__(self):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("framework.log", mode='w')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        con=logging.StreamHandler(sys.stdout,)
        con.setFormatter(formatter)
        self.logger.addHandler(con)
        self.loadName = config.loadDetails['loadName']
        self.logPath = os.popen("pwd").read().strip('\n')+"/"+self.loadName
        self.currentPath = os.system("mkdir -p %s"%(self.logPath))
        self.logger.debug("Entering Config.py ")
        #os.system("cp /tmp/config.py %s"%(self.logPath))
        self.logger.debug("config.py ")
        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']
        #SipAutoTesterObj=SipAutoTester.SipAutoTester(self.logPath)
        #self.logger.debug("SWMRF is Up and Running ")

    def checkSetupHealth(self):

        while True:
            time.sleep(3)
            healthCheckObj=healthCheck.ProcessCheck()
            if healthCheckObj.mrfHealthCheck() !=0 :
                self.logger.error("SWMRF is unreachable ")
                sys.exit()
            else:
                self.logger.debug("SWMRF is Up and Running ")

    def startSAT(self):
        SipAutoTesterObj = SipAutoTester.SipAutoTester(self.logPath)
        resultSAT = SipAutoTesterObj.startSAT()
        return resultSAT

    def checkSetupHealthThread(self):

        threadProcess = threading.Thread(target=self.checkSetupHealth)
        threadProcess.setDaemon(True)
        threadProcess.start()
        self.logger.debug("SWMRF is Up and Running ")

    def topMrf(self):

        topProcessObject = topProcess.topProcess()
        objMSConfig.copytopscript()
        topProcessObject.startTop()
        print "topMrf"

    def topThread(self):

        topThreadProcess = threading.Thread(target=self.topMrf)
        topThreadProcess.setDaemon(True)
        topThreadProcess.start()
        time.sleep(3)
        print "top Mrf"

    def clearMrfLog(self):

        ClearMrfLogObj=ClearMrfLog.ClearMrfLog()
        ClearMrfLogObj.clearSysLog()
        time.sleep(3)
        self.logger.debug("MRF log is cleared ")

    def copyLogs(self):

        SSH_NEWKEY = r'(?i)are you sure you want to continue connecting \(yes/no\)\?'
        COMMAND_PROMPT = '[#] '
        child1=pexpect.spawn("scp  %s@%s:/var/log/messages\{,\.*\}  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
        iii = child1.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
        if iii == 0:
            print "scp timeout"
        elif iii == 1:
            child1.sendline ('yes')
            child1.expect ([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
            child1.sendline('%s'%(self.mrfPassword))
            #print("In scp 1....")
        elif iii == 2:
            child1.sendline('%s'%(self.mrfPassword))
            child1.expect(['#', pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
            #print("In scp 2....")
        elif iii==3:
            pass

        statfile = '/var/opt/swms/stats/statistics.txt'
        child1=pexpect.spawn("scp  %s@%s:%s  %s"%(self.mrfUserName, self.mrfIp, statfile, self.logPath))
        iii = child1.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
        if iii == 0:
            print "scp timeout"
        elif iii == 1:
            child1.sendline ('yes')
            child1.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
            child1.sendline('%s'%(self.mrfPassword))
            #print("In scp 1....")
        elif iii == 2:
            child1.sendline('%s'%(self.mrfPassword))
            child1.expect(['#',pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
            #print("In scp 2....")
        elif iii==3:
            pass

        objtop = topProcess.topProcess()
        objtop.killTOPScript()

        child1=pexpect.spawn("scp  %s@%s:/root/top.txt  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
        iii = child1.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
        if iii == 0:
            print "scp timeout"
        elif iii == 1:
            child1.sendline ('yes')
            child1.expect ([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
            child1.sendline('%s'%(self.mrfPassword))
            #print("In scp 1....")
        elif iii == 2:
            child1.sendline('%s'%(self.mrfPassword))
            child1.expect(['#',pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', COMMAND_PROMPT, pexpect.EOF])
            #print("In scp 2....")
        elif iii==3:
            pass

        os.system("mv /root/*dat %s"%(self.logPath))


if __name__ == '__main__':

    obj = mainProgram()
    objMSConfig.copytopscript()

    def reRun(obj):

        obj.clearMrfLog()
        obj.topThread()
        resultSAT = obj.startSAT()
        print "SAT Result = " + str(resultSAT)
        if resultSAT:
            pass
        else:
            print "Going for reRun"
            reRun(obj)

    reRun(obj)
    obj.copyLogs()

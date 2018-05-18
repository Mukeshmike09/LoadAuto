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



class LoadSeries:
	def __init__(self):
                self.logger = logging.getLogger()
                self.logger.setLevel(logging.DEBUG)
                fh = logging.FileHandler("framework.log",mode='w')
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)
		con=logging.StreamHandler(sys.stdout,)
		con.setFormatter(formatter)
        	self.logger.addHandler(con)
		
		self.loadName=config.loadDetails['loadName']
		self.logPath=os.popen("pwd").read().strip('\n')+"/"+self.loadName
		self.currentPath = os.system("mkdir -p %s"%(self.logPath))
		self.logger.debug("Entering Config.py ")
		#os.system("cp /tmp/config.py %s"%(self.logPath))
		self.logger.debug("config.py ")
		self.mrfIp=config.swMrfCredentials['mrfIp']	
		self.mrfUserName=config.swMrfCredentials['mrfUserName']
		self.mrfPassword=config.swMrfCredentials['mrfPassword']
	        
		#SipAutoTesterObj=SipAutoTester.SipAutoTester(self.logPath)	
		self.logger.debug("SWMRF is Up and Running ")

	def checkSetupHealth(self):
		while True:
			time.sleep(3)
			healthCheckObj=healthCheck.ProcessCheck()
			if healthCheckObj.mrfHealthCheck() !=0 :
	        	        self.logger.error("SWMRF is unreachable ")
				sys.exit()
			else:
	                	self.logger.debug("SWMRF is Up and Running ")
	def checkSetupHealthThread(self):
		threadProcess=threading.Thread(target=self.checkSetupHealth)
		threadProcess.setDaemon(True)
		threadProcess.start()
		#threadProcess.join()
		#print "sleep for 30"
		#time.sleep(30)
		#print "sleep completed"
                self.logger.debug("SWMRF is Up and Running ")
	def topMrf(self):
		topProcessObject=topProcess.topProcess()
		topProcessObject.startTop()
		print "topMrf"

	def topThread(self):
		topThreadProcess=threading.Thread(target=self.topMrf)
		topThreadProcess.setDaemon(True)
		topThreadProcess.start()
		time.sleep(3)
		print "top Mrf"
	def clearMrfLog(self):
		ClearMrfLogObj=ClearMrfLog.ClearMrfLog()
		ClearMrfLogObj.clearSysLog()
		time.sleep(3)
		self.logger.debug("MRF log is cleared ")
	def startSAT(self):
		SipAutoTesterObj=SipAutoTester.SipAutoTester(self.logPath)
		SipAutoTesterObj.startSAT()
	def copyLogs(self):
		SSH_NEWKEY = r'(?i)are you sure you want to continue connecting \(yes/no\)\?'
		child1=pexpect.spawn("scp  %s@%s:/var/log/messages.*  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
		print "here"
                iii = child1.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                if iii == 0:
                    print "scp timeout"
                elif iii == 1:
                    child1.sendline ('yes')
                    child1.expect ([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    #child1.sendline('zac#61')
                    child1.sendline('%s'%(self.mrfPassword))
                    print("In scp 1....")
                elif iii == 2:
                    child1.sendline('%s'%(self.mrfPassword))
                    child1.expect(['#',pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    print("In scp 2....")
                elif iii==5:
                    print "EOF"

		child2=pexpect.spawn("scp  %s@%s:/var/log/messages  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
		print self.logPath
                iiii = child2.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                if iiii == 0:
                    print "scp timeout"
                elif iiii == 1:
                    child2.sendline ('yes')
                    child2.expect ([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    child2.sendline('%s'%(self.mrfPassword))
                    print("In scp 1....")
                elif iiii == 2:
                    child2.sendline('%s'%(self.mrfPassword))
                    child2.expect(['#',pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    print("In scp 2....")
                elif iiii == 4:
                    print "EOF"
		
		stat=pexpect.spawn("scp  %s@%s:/var/opt/swms/stats/statistics.txt  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
		#child2=pexpect.spawn("scp  %s@%s:/var/log/messages  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
                j = stat.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                if j == 0:
                    print "scp timeout"
                elif j == 1:
                    stat.sendline ('yes')
                    stat.expect ([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    stat.sendline('%s'%(self.mrfPassword))
                    print("In scp 1....")
                elif j == 2:
                    stat.sendline('%s'%(self.mrfPassword))
                    stat.expect(['#',pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    print("In scp 2....")
                elif j == 4:
                    print "EOF"
                
		top=pexpect.spawn("scp  %s@%s:/root/top.txt  %s"%(self.mrfUserName,self.mrfIp,self.logPath))
                print "mukesh"
                k = top.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                if k == 0:
                    print "scp timeout"
                elif k == 1:
                    top.sendline ('yes')
                    top.expect ([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    top.sendline('%s'%(self.mrfPassword))
                    print("In scp 1....")
                elif k == 2:
                    top.sendline('%s'%(self.mrfPassword))
                    top.expect(['#',pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password', "tcpdump_*", '\$',pexpect.EOF])
                    print("In scp 2....")  
                elif k == 4:
                    print "EOF"
		os.system("mv /root/*dat %s"%(self.logPath))


                		
obj=LoadSeries()
#obj.checkSetupHealthThread()
obj.clearMrfLog()
obj.topThread()
obj.startSAT()
time.sleep(2)
obj.copyLogs()

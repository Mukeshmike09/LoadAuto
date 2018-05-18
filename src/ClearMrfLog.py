import pexpect
import time
import os
import config
import logging

class ClearMrfLog:
	def __init__(self):
		self.mrfIp=config.swMrfCredentials['mrfIp']
                self.mrfUserName=config.swMrfCredentials['mrfUserName']
                self.mrfPassword=config.swMrfCredentials['mrfPassword']
		self.logger = logging.getLogger("ClearMrfLog.py")
		self.logger.debug("clearing MRF Log ")
	def clearSysLog(self):
		SSH_NEWKEY = r'(?i)are you sure you want to continue connecting \(yes/no\)\?'
		try:
		  m=pexpect.spawn('ssh %s@%s'%(self.mrfUserName,self.mrfIp))
		except IOError:
		  print "there is problem"
		else:
		  m.timeout = 300
		  first = m.expect(['password:',SSH_NEWKEY, '#'])
		  if (first == 0):
		      m.sendline('%s'%(self.mrfPassword))
		      time.sleep(2)
		      index =  m.expect(['password:','#'])
		      if (index == 1):
		         print "connected"
		      elif (index == 0):
		         print "password problem"
		  elif (first == 1):
		      m.sendline('yes')
		      m.expect ('password:')
		      m.sendline('mypassword')
		      time.sleep(2)
		      index =  m.expect(['password:','#'])
		      if (index == 1):
		         print "password connected"
		      elif (index == 0):
		         print "wrong password."
		  elif (first == 2):
		         print  "password connected"
		  
		  m.sendline('cat /dev/null > /var/log/messages')
		  m.sendline('rm -rf /var/log/messages.*')
		  i=m.expect([pexpect.EOF,'#']) 
		  if i==0:
		      print('Syslog clearing failed!!!')
		      time.sleep(2)
		  elif i==1:
		      print('Syslog cleared successfully')
		  m.sendline('cat /dev/null > /var/opt/swms/stats/statistics.txt')
		  i=m.expect([pexpect.EOF,'#'])
		  if i==0:
		      print('statistics clearing failed!!!')
		      time.sleep(2)
		  elif i==1:
		      print('statistics cleared successfully')
		

                  

                  m.sendline('cat /dev/null > top.txt')
                  i=m.expect([pexpect.EOF,'#'])
                  if i==0:
                      print('top clearing failed!!!')
                      time.sleep(2)
                  elif i==1:
                      print('top cleared successfully')
                  m.sendline('cat /dev/null > top.txt')
                  i=m.expect([pexpect.EOF,'#'])
                  if i==0:
                      print('top clearing failed!!!')
                      time.sleep(2)
                  elif i==1:
                      print('top cleared successfully')





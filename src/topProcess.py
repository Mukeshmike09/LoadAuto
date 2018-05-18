import pexpect
import time
import os
import config

class topProcess:

    def __init__(self):
        self.mrfIp=config.swMrfCredentials['mrfIp']
        self.mrfUserName=config.swMrfCredentials['mrfUserName']
        self.mrfPassword=config.swMrfCredentials['mrfPassword']
        self.loadDur=config.loadDurationDetails['loadduration']

    def startTop(self):
        SSH_NEWKEY = r'(?i)are you sure you want to continue connecting \(yes/no\)\?'
        try:
            m=pexpect.spawn("ssh %s@%s"%(self.mrfUserName,self.mrfIp))
        except IOError:
            print "there is problem"
        else:
            print (self.loadDur)
            m.timeout = int(self.loadDur)
            first = m.expect(['password:',SSH_NEWKEY, '#'])
            if first == 0:
                m.sendline('%s'%(self.mrfPassword))
                time.sleep(2)
                index =  m.expect(['password:','#'])
                if index == 1:
                    print "connected"
                elif index == 0:
                    print "password problem"
            elif first == 1:
                m.sendline('yes')
                m.expect ('password:')
                m.sendline('mypassword')
                time.sleep(2)
                index =  m.expect(['password:','#'])
                if index == 1:
                    print "password connected"
                elif index == 0:
                    print "wrong password."
            elif first == 2:
                print  "password connected"
            m.sendline('while true; do top -Mbn 1; cat /proc/meminfo; free -m; slabtop -s c -o; ps auxk rss | \
                grep -v \' 0.0  0.0      0     0\'; sleep 15; done |tee /root/top.txt')
            print "hello"
            i=m.expect([pexpect.EOF,'#',pexpect.TIMEOUT])
            print "hello1"
            #m.sendlinei('')
            if i==0:
                print('top!!!')
                time.sleep(2)
            if i==1:
                print('c what happen')
                time.sleep(2)
            elif i==2:
                print('top success')

#obj=topProcess()
#obj.startTop()
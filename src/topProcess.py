import pexpect
import time
import config

class topProcess:

    def __init__(self):
        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']
        self.loadDur = config.loadDurationDetails['loadduration']

    def startTop(self):
        SSH_NEWKEY = r'(?i)are you sure you want to continue connecting \(yes/no\)\?'
        try:
            m = pexpect.spawn("ssh %s@%s"%(self.mrfUserName,self.mrfIp))
        except IOError:
            print "There is problem in doing SSH. "
        else:
            print (self.loadDur)
            m.timeout = int(self.loadDur)
            first = m.expect(['password:', SSH_NEWKEY, '#'])
            if first == 0:
                m.sendline('%s' %(self.mrfPassword))
                time.sleep(2)
                index = m.expect(['password:', '#'])
                if index == 1:
                    print "Connected to SUT to capture TOP "
                elif index == 0:
                    print "Wrong password "
            elif first == 1:
                m.sendline('yes')
                ssh_first = m.expect(['password:', '#'])
                if ssh_first == 1:
                    m.sendline('%s' % (self.mrfPassword))
                    time.sleep(2)
                    index = m.expect(['password:', '#'])
                    if index == 1:
                        print "Connected to SUT to capture TOP "
                    elif index == 0:
                        print "Wrong password "
            elif first == 2:
                print "Connected to SUT to capture TOP "
            print "Running TOP script"
            m.sendline('nohup /root/loadtop.sh &')
            i = m.expect([pexpect.EOF, '#', pexpect.TIMEOUT])
            if i == 1:
                print "Killed top script. "
                m.sendline(" ")
                m.expect([pexpect.EOF, '#', pexpect.TIMEOUT])
            else:
                print "There is some problem while starting the TOP script. "

    def killTOPScript(self):

        SSH_NEWKEY = r'(?i)are you sure you want to continue connecting \(yes/no\)\?'
        try:
            m = pexpect.spawn("ssh %s@%s"%(self.mrfUserName,self.mrfIp))
        except IOError:
            print "There is problem in doing SSH. "
        else:
            print (self.loadDur)
            m.timeout = int(self.loadDur)
            first = m.expect(['password:', SSH_NEWKEY, '#'])
            if first == 0:
                m.sendline('%s' %(self.mrfPassword))
                time.sleep(2)
                index = m.expect(['password:', '#'])
                if index == 1:
                    print "Connected to SUT to stop TOP "
                elif index == 0:
                    print "Wrong password "
            elif first == 1:
                m.sendline('yes')
                ssh_first = m.expect(['password:', '#'])
                if ssh_first == 1:
                    m.sendline('%s' % (self.mrfPassword))
                    time.sleep(2)
                    index = m.expect(['password:', '#'])
                    if index == 1:
                        print "Connected to SUT to stop TOP "
                    elif index == 0:
                        print "Wrong password "
            elif first == 2:
                print "Connected to SUT to stop TOP "

            m.sendline("ps -eaf|grep '/root/loadtop.sh' | grep -v 'grep'  | awk -F' ' '{print $2}' | xargs kill -9")
            ii = m.expect([pexpect.EOF, '#', pexpect.TIMEOUT])
            if ii == 1:
                print "Killed top script. "
                m.sendline(" ")
                m.expect([pexpect.EOF, '#', pexpect.TIMEOUT])
            else:
                print "There is some problem while killing the TOP script. "

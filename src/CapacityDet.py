#!/usr/bin/python

import config
import commands


class CapacityDet:
    def __init__(self, number):
        self.number = number
        self.loadAT = config.loadDetails['ATFile']
        self.SATPath = config.SATDetails['SATPath']

    def Dynamiccheck(self):
        # NumofConn = str(os.popen('grep NumberOfConnections= %s%s'%(self.SATPath,self.loadAT)).read()).strip("\n")
        NumofConn1 = commands.getoutput('grep "^NumberOfConnections=" %s%s | tail -1' % (self.SATPath, self.loadAT))
        # number1=int(self.number)
        NumofConf1 = commands.getoutput('grep "^NumberOfConferences=" %s%s | tail -1' % (self.SATPath, self.loadAT))
        # NumofConf = str(os.popen('grep NumberOfConferences= %s%s'%(self.SATPath,self.loadAT)).read()).strip("\n")
        NumofConn = NumofConn1.split("=")[1]
        NumofConf = NumofConf1.split("=")[1]
        CurrentTotalofPorts = int(NumofConn) * int(NumofConf)
        OneofDsp = CurrentTotalofPorts / int(self.number)
        UpdateValOfPorts = int(OneofDsp + 1) * 70
        print "UpdateValOfPorts", UpdateValOfPorts
        UpdateValOfConn = int(UpdateValOfPorts) / int(NumofConn)
        print "UpdateValOfConf", UpdateValOfConn
        commands.getoutput(
            "sed -i 's/%s/NumberOfConferences=%s/g' %s%s" % (NumofConf1, UpdateValOfConn, self.SATPath, self.loadAT))

    def decreaseThePorts(self):
        NumofConf1 = commands.getoutput('grep NumberOfConferences= %s%s' % (self.SATPath, self.loadAT))
        NumofConf = NumofConf1.split("=")[1]
        UpdateValOfConf = int(NumofConf) - 4
        commands.getoutput(
            "sed -i 's/%s/NumberOfConferences=%s/g' %s%s" % (NumofConf1, UpdateValOfConf, self.SATPath, self.loadAT))

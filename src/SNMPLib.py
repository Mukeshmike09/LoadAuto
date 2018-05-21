#!/usr/bin/python
import subprocess
import config

class SNMPLib:
    def __init__(self):
        self.MSMYPATH = '/root/.snmp/'
        self.SUTIP = config.swMrfCredentials['mrfIp']

    ################################################   FUNCTION TO GET ANY SNMP MIB   #################################
    def snmpgetcheck(self, Mibvalue, value):

        internalreponse = ''
        snmpout_data = []
        snmpout = subprocess.Popen(
            'snmpget -Oq -c CONV -v 2c -r 0 -t 30 -m %sMS.my %s %s' % (self.MSMYPATH, self.SUTIP, Mibvalue), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while snmpout.returncode is None:
            snmpout.poll()
            snmpout_data = snmpout.communicate()

        if snmpout.returncode == 0:
            if str(snmpout_data[0]).find('%s' % (value)) != -1:
                self.result = 'PASS'
            else:
                self.result = 'FAIL'

        elif snmpout.returncode > 0:
            self.result = 'FAIL'

        if self.result == 'FAIL':
            return False

        return True

    ################################################   FUNCTION TO GET ANY SNMP MIB AND RETURN THE VALUE  #############

    def snmpget(self, Mibvalue):

        response = []
        actualresponse = []
        snmpout_data = []
        print "snmpget -Oq -c CONV -v 2c -r 0 -t 30 -m " + self.MSMYPATH + "/MS.my " + self.SUTIP + " " + Mibvalue
        snmpout = subprocess.Popen(
            'snmpget -Oq -c CONV -v 2c -r 0 -t 30 -m %sMS.my %s %s' % (self.MSMYPATH, self.SUTIP, Mibvalue), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while snmpout.returncode is None:
            snmpout.poll()
            snmpout_data = snmpout.communicate()

        if (snmpout.returncode == 0):
            response = str(snmpout_data[0]).split(' ')
            self.result = 'PASS'
        elif (snmpout.returncode > 0):
            self.result = 'FAIL'

        actualresponse = response[1].split('\n')

        return str(actualresponse[0])

    ########   FUNCTION TO DO SNMP SET COMMAND AND VERIFY THE RESULT  #################################################

    def snmpset(self, Mibvalue, value, Type):

        #originalvalue = self.snmpget(Mibvalue)
        snmpout_data = []
        print "snmpset -Oq -c CONV -v 2c -m " + self.MSMYPATH + "/MS.my " + self.SUTIP + " " + Mibvalue + " " + Type + \
              " " + value
        snmpout = subprocess.Popen(
            'snmpset -Oq -c CONV -v 2c -m %sMS.my %s %s %s "%s"' % (self.MSMYPATH, self.SUTIP, Mibvalue, Type, value),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while snmpout.returncode is None:
            snmpout.poll()
            snmpout_data = snmpout.communicate()
        if snmpout.returncode == 0:
            responce = str(snmpout_data[0]).split(' ')
            actualresponse = responce[1].split('\n')

            if actualresponse[0] == value:
                self.result = 'PASS'
            else:
                self.result = 'FAIL'
        elif snmpout.returncode > 0:
            self.result = 'FAIL'

    ############     THIS FUNCTION IS USED TO SEE IF THE EXPECTED RESULT IS CORRECT OR NOT   ##########################

    def checksnmpresult(self, expected):

        if self.result == expected:
            self.result = 'PASS'
        else:
            self.result = 'FAIL'

    ############     THIS FUNCTION IS USED TO SEE IF THE EXPECTED RESULT IS CORRECT OR NOT   ##########################

    def getMSaudiocores(self):

        NumMpCores = self.snmpget('caNumMpCores.0')
        NumVxmlCores = self.snmpget('caNumVxmlCores.0')
        NumVideoCores = self.snmpget('caNumVideoCores.0')
        NumHdEncCores = self.snmpget('caNumHdEncCores.0')

        return str(int(NumMpCores) - (int(NumVxmlCores) + int(NumVideoCores) + int(NumHdEncCores)))





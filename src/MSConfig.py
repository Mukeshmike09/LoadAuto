from SNMPLib import SNMPLib

snmpobj = SNMPLib()

class MSConfig:

    def __init__(self):
        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']

    def checkmscores(self):

        audiocores = snmpobj.getMSaudiocores()

        if audiocores == '0':
            print "There are no audio cores, Setting default core (equal audio & video)"
            allocated = int(snmpobj.snmpget('caNumMpCores.0'))
            if allocated >= 4:
                snmpobj.snmpset('caNumVxmlCores.0', '0', 'u')
                snmpobj.snmpset('caNumHdEncCores.0', '0', 'u')
                snmpobj.snmpset('caNumVideoCores.0', str(allocated/2), 'u')
            else:
                print "SUT has less than 4 cores"

    def refactorcores(self, acheivedports='1000', video = False, conf = False):
        if acheivedports > 1000:
            print "Number of acheved ports are more than 1000, refactoring SUT cores"



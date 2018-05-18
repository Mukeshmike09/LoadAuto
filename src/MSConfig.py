from SNMPLib import SNMPLib

class MSConfig:

    def __init__(self):
        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']

    def checkMScores(self):
        audiocores = SNMPLib.getMSaudiocores()

        if audiocores == '0':
            print "There are no audio cores"

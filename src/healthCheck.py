#!/usr/bin/python
import subprocess
import logging
import config
import time

class ProcessCheck:

    def __init__(self):

        self.mrfIp = config.swMrfCredentials['mrfIp']
        self.mrfUserName = config.swMrfCredentials['mrfUserName']
        self.mrfPassword = config.swMrfCredentials['mrfPassword']
        self.logger = logging.getLogger("healthCheck > ProcessCheck")

    def mrfHealthCheck(self):
        time.sleep(10)
        self.logger.info("checking MRF..... ")
        pingObj = subprocess.call(['ping','-c', '3','%s'%(self.mrfIp)])    ###returns 0 if success
        self.logger.info("Logging MRF..... ")
        return pingObj

#obj=ProcessCheck()
#obj.healthCheckLogger()
#obj.mrfHealthCheck()
#obj.add()

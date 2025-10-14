#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2024 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************

import os
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from raft.framework.plugins.ut_raft import utHelperClass
from raft.framework.core.logModule import logModule
from raft.framework.plugins.ut_raft.utPlayer import utPlayer
from raft.framework.plugins.ut_raft.utUserResponse import utUserResponse

class initialSetupTests_test3_verify_westeros(utHelperClass):


    def __init__(self, log:logModule=None):
        """
        Initializes the initialSetupTests_test3_verify_westeros test .
        Args:
            None.
        """

        self.testName  = "test3_verify_westeros"
        self.moduleName = "initialSetupTests"
        self.qcID = '3'
        self.testsuite  = "L3 initialSetupTests"

        super().__init__(self.testName, self.qcID, log)

    def testFunction(self):
        """
        This function will test the lsmod command
        Args:
            None.
        """

        self.log.stepStart(f'initialSetupTests_test3_verify_westeros')

        # Open Session for hal test
        self.player_session = self.dut.getConsoleSession("ssh_player")
        socVendor = self.cpe.get("soc_vendor")
        self.testPlayer = utPlayer(self.player_session, socVendor) #sends all the prerequisite for westeros
        time.sleep(3)
        self.player_session.write("westeros_test") #send westeros test app
        output = self.player_session.read_all()
        self.log.step(f'Output: {output}')
        time.sleep(5)
        self.testUserResponse = utUserResponse()
        result = self.testUserResponse.getUserYN(f"Is A Triangular display visible on the HDMI? (Y/N):")
        self.testPlayer.stop()
        self.player_session.close()  # Close the session
        self.log.stepResult(result, f'Test to verify Westeros Test App')

        return

if __name__ == '__main__':
    summerLogName = os.path.splitext(os.path.basename(__file__))[0] + "_summery"
    summeryLog = logModule(summerLogName, level=logModule.INFO)
    test = initialSetupTests_test3_verify_westeros(summeryLog)
    test.run(False)

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

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from raft.framework.plugins.ut_raft import utHelperClass
from raft.framework.core.logModule import logModule

class initialSetupTests_test1_verify_build_version(utHelperClass):


    def __init__(self, log:logModule=None):
        """
        Initializes the initialSetupTests_test1_verify_build_version test .

        Args:
            None.
        """

        self.testName  = "test2_verify_build_version"
        self.moduleName = "initialSetupTests"
        self.qcID = '1'
        self.testsuite  = "L3 initialSetupTests"

        super().__init__(self.testName, self.qcID, log)


    def testFunction(self):
        """
        This function will test the build version of the flashed image

        Args:
            None.
        """

        self.log.stepStart(f'initialSetupTests_test2_verify_build_version using serial console')

        # Open Session for hal test
        self.hal_session = self.dut.getConsoleSession("serial")
        self.hal_session.flush()
        self.hal_session.write("cat /version.txt")  # Send the command
        output = self.hal_session.read_until("root")  # Read all output until "root"
        self.hal_session.close()  # Close the session
        result = input("Please enter build version to validate: ")
        assert output.__contains__(result)  # Verify the output
        self.log.stepResultMessage(f'Build Details : {output}')

        return

if __name__ == '__main__':
    summerLogName = os.path.splitext(os.path.basename(__file__))[0] + "_summery"
    summeryLog = logModule(summerLogName, level=logModule.INFO)
    test = initialSetupTests_test1_verify_build_version(summeryLog)
    test.run(False)
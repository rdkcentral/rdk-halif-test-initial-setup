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
import re
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")

from raft.framework.plugins.ut_raft import utHelperClass
from raft.framework.core.logModule import logModule

class initialSetupTests_test2_verify_lsmod(utHelperClass):


    def __init__(self, log:logModule=None):
        """
        Initializes the initialSetupTests_test2_Verify_lsmod test .

        Args:
            None.
        """

        self.testName  = "test2_Verify_lsmod"
        self.moduleName = "initialSetupTests"
        self.qcID = '2'
        self.testsuite  = "L3 initialSetupTests"

        super().__init__(self.testName, self.qcID, log)


    def testFunction(self):
        """
        This function will test the lsmod command

        Args:
            None.
        """

        self.log.stepStart(f'initialSetupTests_test2_Verify_lsmod')

        # Open Session for hal test
        self.hal_session = self.dut.getConsoleSession("ssh_hal_test")
        self.hal_session.write("lsmod")  # Send the command
        output = self.hal_session.read_all()  # Read all output
        self.hal_session.close()  # Close the session
        self.log.step(f'Output of lsmod: {output}')
        assert re.search(r'Module\s+Size\s+Used by', output)  # Verify the output using regex

        return

if __name__ == '__main__':
    summerLogName = os.path.splitext(os.path.basename(__file__))[0] + "_summery"
    summeryLog = logModule(summerLogName, level=logModule.INFO)
    test = initialSetupTests_test2_verify_lsmod(summeryLog)
    test.run(False)
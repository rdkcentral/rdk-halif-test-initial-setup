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
from raft.framework.plugins.ut_raft.utUserResponse import utUserResponse
from raft.framework.plugins.ut_raft.configRead import ConfigRead

class initialSetupTests_test4_verify_miracast_test(utHelperClass):


    def __init__(self, log:logModule=None):
        """
        Initializes the initialSetupTests_test2_Verify_lsmod test .
        Args:
            None.
        """

        self.testName  = "test4_Verify_Miracast"
        self.moduleName = "initialSetupTests"
        self.qcID = '4'
        self.testsuite  = "L3 initialSetupTests"
        self.testConfigPath = os.path.join(dir_path, "miracast_Config.yml")
        
        # Create user response Class
        self.testUserResponse = utUserResponse()

        super().__init__(self.testName, self.qcID, log)
        
        self.soc_vendor = self.cpe.get("soc_vendor")
        
        self.configSetup = ConfigRead(self.testConfigPath, self.soc_vendor)

    
    def testVerify(self, manual=False, wifi=False, cast=False, devicename="None"):
        if manual == True and wifi == True:
            return self.testUserResponse.getUserYN(f"Is mobile phone and device connected to same wifi network and Cast enabled on mobile? (Y/N):")
        elif manual == True and cast == True:
            return self.testUserResponse.getUserYN(f"Is device {devicename} listed on mobile? (Y/N):")
        else :
            #TODO: Add automation verification methods
            return False


    def testFunction(self):
        """
        This function will test the Miracast feature
        Args:
            None.
        """

        self.log.stepStart(f'initialSetupTests_test4_Verify_Miracast')

        # Open Session for hal test
        self.hal_session = self.dut.getConsoleSession("ssh_hal_test")

        self.hal_session.write("ifconfig wlan0")
        self.hal_session.write("iw list")
        feature_support = self.hal_session.read_all()

        #Check whether P2P feature is supported or not
        if "P2P-client" or "P2P-GO" in feature_support:

            if "inet addr" in feature_support:

                config = self.configSetup.p2p0

                #Add the p2p interface command from config
                if config.p2p_interface:
                    for interface in config.p2p_interface:
                        self.hal_session.write(interface)

                cli_output = self.hal_session.read_all()  # Read all output

                #Checks whether Interactive mode is available or not
                if "Could not connect to wpa_supplicant" not in cli_output:
                    for cmd in config.p2p_commands:
                        if cmd == "SET device_name":
                            devicename = f"Miracast_{self.soc_vendor}"
                            cmd = f"SET device_name {devicename}"
                        #Executes the P2P commands
                        self.hal_session.write(cmd)

                    result = self.testVerify(True, True)
                    self.log.stepResult(result, 'Device and mobile connected to same network and Cast is enabled on mobile')

                    result = self.testVerify(True, False, True, devicename)
                    self.log.stepResult(result, f'{devicename} listed in cast list')
                    
                    #Through "GET device_name" verifying the name
                    self.hal_session.write("GET device_name")
                    get_devicename = self.hal_session.read_all()

                    if devicename in get_devicename:
                        self.log.stepResult(True, f'Output of GET devicename: {devicename}')
                    else:
                        self.log.stepResult(False, f'SET and GET devicename is not matched {devicename}')
                else:
                    self.log.stepResult(False, 'Could not connect to wpa_supplicant')
            else:
                self.log.stepResult(False, 'Please connect to Wifi before start the test')
        else:
            self.log.stepResult(False, 'P2P feature is not supported')

        self.hal_session.close()  # Close the session

        return

if __name__ == '__main__':
    summerLogName = os.path.splitext(os.path.basename(__file__))[0] + "_summery"
    summeryLog = logModule(summerLogName, level=logModule.INFO)
    test = initialSetupTests_test4_verify_miracast_test(summeryLog)
    test.run(False)
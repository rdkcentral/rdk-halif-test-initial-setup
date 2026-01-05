# Initial Setup L3 Python Test Procedure

## Table of Contents

- [Acronyms, Terms and Abbreviations](#acronyms-terms-and-abbreviations)
- [Setting Up Test Environment](#setting-up-test-environment)
- [Run Test Cases](#run-test-cases)
- [Test Setup Connections](#test-setup-connections)
- [Test Cases](#test-cases)
  - [initialsetuptests_test1_verify_build_version.py](#initialsetuptests_test1_verify_build_versionpy)
  - [nitialsetuptests_test2_verify_lsmod.py](#initialsetuptests_test2_verify_lsmodpy)
  - [initialsetuptests_test3_verify_westeros.py](#initialsetuptests_test3_verify_westerospy)
  - [initialsetuptests_test4_verify_miracast_test.py](#initialsetuptests_test4_verify_miracast_testpy)
## Acronyms, Terms and Abbreviations

- `HAL`    - Hardware Abstraction Layer
- `L3`     - Level 3 Testing
- `DUT`    - Device Under Test
- `RAFT`   - Rapid Automation Framework for Testing
- `YAML`   - YAML Ain't Markup Language
- `LAN`    - Local Area Network
- `SSID`   - Service Set Identifier
- `IP`     - Internet Protocal

## Setting Up Test Environment

To execute `HAL` `L3` Python test cases, need a Python environment. Follow these steps mentioned in [HPK Public Documentation](https://github.com/rdkcentral/rdk-hpk-documentation/blob/main/README.md)

### Update Configuration Files

#### Rack Configuration File

Example Rack configuration File: [example_rack_config.yml](./host/tests/configs/example_rack_config.yml)

For more details refer [RAFT](https://github.com/rdkcentral/python_raft/blob/1.0.0/README.md) and [example_rack_config.yml](https://github.com/rdkcentral/python_raft/blob/1.0.0/examples/configs/example_rack_config.yml)

In this file, update the configuration to define the console sessions for the `DUT` :

|Console Session|Description|
|---------------|-----------|
|default|This session is used for basic operations, such as verifying the device status and retrieving the MAC address|
|ssh_hal_test|Utilized by the `lsmod` and `miracast`testcase|
|ssh_player|Utilized by the `westeros` test|

```yaml
rackConfig:
    rack1:
        name: "rack1"
        description: "example config at my desk"
        slot1:
            # [ name: "required", description: "optional"]
            name: "slot1"
            devices:
                # [ devices: ]
                # [ type: "serial": port: "COM7" baudRate: "(default)115200" dataBits: "optional(8)" stopBits: "optional(1)" parity: "optional(None)" FlowControl: "optional(None)" ]
                # [ type: "ssh": port: 22 username: "test" password: "test" ]
                # [ type: "telnet": port: 23 username: "test" password: "test" ]
                - dut:
                    ip: "127.0.0.1"  # IP Address of the ADA Hub
                    description: "local PC"
                    platform: "panel"
                    consoles:
                        - default:
                            type: "ssh"
                            port: 20022
                            username: "root"
                            ip: "" #IP address
                        - ssh_player:
                            type: "ssh"
                            port: 20022
                            username: "root"
                            ip: "" #IP address
                            password: ''
                        - ssh_hal_test:
                            type: "ssh"
                            port: 10022
                            username: "root"
                            ip: "" #IP address
                            password: ''
                        - serial:
                             type: "serial"
                             port: "COM3"
                             baudRate: "115200"
                             dataBits: "8"
                             stopBits: "1"
                             parity: None
                             FlowControl: None
```

#### Device Configuration File

Example Device configuration File: [deviceConfig.yml](./host/tests/configs/deviceConfig.yml)

For more details refer [RAFT](https://github.com/rdkcentral/python_raft/blob/1.0.0/README.md) and [example_device_config.yml](https://github.com/rdkcentral/python_raft/blob/1.0.0/examples/configs/example_device_config.yml)

Update the target directory where `HAL` binaries will be copied into the device. Also, map the profile to the source/sink settings `YAML` file path.

Ensure the platform should match with the `DUT` platform in [Rack Configuration](#rack-configuration-file)

```yaml
deviceConfig:
    cpe1:
        platform:   "panel" # Must match the platform in example_rack_config.yml
        model:      "uk"
        soc_vendor: "xx" # Must match the soc available in miracast_Config.yml
        target_directory: "/opt/xx"  # This is not very important in this repo as no binary is copied to target
        prompt: "" # Prompt string on console


```

#### Test Setup Configuration File

Miracast configuration File: [miracast_Config.yml](./host/tests/L3_TestCases/miracast_Config.yml)

```yaml
realtek: # Platform name
  p2p0: 
    p2p_interface:
      - wpa_supplicant -i p2p0 -D nl80211 -c /opt/wpa-supplicant.conf -B -d
      - wpa_cli -i p2p0
    p2p_commands: 
      - SET device_name
      - SET config_methods pbc
      - SET WIFI_DISPLAY 1
      - P2P_SET disallow_freq 5180-5900
      - freq 5180-5900
      - WFD_SUBELEM_SET 0
      - WFD_SUBELEM_SET 0 000600111c4400c8
      - P2P_FIND
amlogic:
  p2p0: 
    p2p_interface:
      - wpa_supplicant -B -Dnl80211 -c /data/wpa-supplicant.conf -ip2p0 -d -t -f /opt/logs/wpa_supplicant.log
      - wpa_cli -i p2p0
    p2p_commands: 
      - SET device_name
      - SET config_methods pbc
      - SET WIFI_DISPLAY 1
      - P2P_SET disallow_freq 5180-5900
      - freq 5180-5900
      - WFD_SUBELEM_SET 0
      - WFD_SUBELEM_SET 0 000600111c4400c8
      - P2P_FIND
```
[initialSetupTests_test4_verify_miracast_test.py](./host/tests/L3_TestCases/initialSetupTests_test4_verify_miracast_test.py), utilizes this yaml file to get the commands for its operation.

## Run Test Cases

Activate python environment

```bash
cd host
./install.sh
source ./activate_venv.sh
./install.sh
```
Once the environment is set up, you can execute the test cases with the following command

```bash
python <TestCaseName.py> --config </PATH>/ut/host/tests/configs/example_rack_config.yml --deviceConfig </PATH>/ut/host/tests/configs/deviceConfig.yml
```

## Test Setup Connections

Make sure the device under test `DUT` is connected to wifi, `LAN` and a `CEC` supported device for waking up from deepsleep before starting the test case.

### Example WIFI Configuration
If the `DUT` supports WPA, follow these steps to configure the `WIFI`:

**Generate the WPA Configuration File:**

Use the router's `SSID` and password to create a configuration file:

```bash
wpa_passphrase <"Router SSID"> <"Passsword" > /data/wpa-supplicant.conf
```

**Start the wpa_supplicant daemon:**
Run the following command to start the `wpa_supplicant` service:

```bash
wpa_supplicant -dd -B -i wlan0 -c /data/wpa-supplicant.conf
```

If still not getting `IP` for `wlan0` bridge interface try:

```bash
ifconfig wlan0 down
ifconfig wlan0 up
```

## Test Cases
### initialSetupTests_test1_verify_build_version.py

#### Platform Support - test01

- Sink/Source

#### Prerequisite - test01

Requires serial connection. Make sure required details are filled in [deviceConfig.yml](./host/tests/configs/deviceConfig.yml) and [example_rack_config.yml](./host/tests/configs/example_rack_config.yml) as explained in [Setting Up Test Environment](#setting-up-test-environment)


#### Test Steps - test01

- Initiate the Test:

  - Select and execute the Python file: **`initialSetupTests_test1_verify_build_version.py`** as described in [Run Test Cases](#run-test-cases)
  - The test will automatically test the build flashed on the device and validate it with build provided by user.

### initialSetupTests_test2_verify_lsmod.py

#### Platform Support - test02

- Sink/Source

#### Prerequisite - test02

Requires ssh connection. Make sure required details are filled in [deviceConfig.yml](./host/tests/configs/deviceConfig.yml) and [example_rack_config.yml](./host/tests/configs/example_rack_config.yml) as explained in [Setting Up Test Environment](#setting-up-test-environment)


#### Test Steps - test02

- Initiate the Test:

  - Select and execute the Python file: **`initialSetupTests_test2_verify_lsmod.py`** as described in [Run Test Cases](#run-test-cases)
  - The test will automatically test lsmod and display output on the console.


### initialSetupTests_test3_verify_westeros.py

#### Platform Support - test03

- Sink/Source

#### Prerequisite - test03

Requires ssh connection. Make sure required details are filled in [deviceConfig.yml](./host/tests/configs/deviceConfig.yml) and [example_rack_config.yml](./host/tests/configs/example_rack_config.yml) as explained in [Setting Up Test Environment](#setting-up-test-environment)


#### Test Steps - test03

- Initiate the Test:

  - Select and execute the Python file: **`initialSetupTests_test3_verify_westeros.py`** as described in [Run Test Cases](#run-test-cases)
  - The test will automatically test westeros test and validates if the triangular display is visible on the HDMI output

### initialSetupTests_test4_verify_miracast_test.py

#### Platform Support - test04

- Sink/Source

#### Prerequisite - test04

Requires ssh connection from wlan0. Make sure required details are filled in [deviceConfig.yml](./host/tests/configs/deviceConfig.yml) and [example_rack_config.yml](./host/tests/configs/example_rack_config.yml) as explained in [Setting Up Test Environment](#setting-up-test-environment)


#### Test Steps - test04

- Initiate the Test:

  - Select and execute the Python file: **`initialSetupTests_test4_verify_miracast_test.py`** as described in [Run Test Cases](#run-test-cases)
  - The test will automatically test miracast feature for supported devices.

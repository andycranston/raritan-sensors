#! /usr/bin/python3
#
# @(!==#) @(#) settempthresholds.py, version 005, 12-august-2019
#
# set the thresholds for all temperatiure sensors on a PDU
#
#
# Links:
#
#   https://help.raritan.com/json-rpc/pdu/v3.5.0/index.html
#   https://help.raritan.com/json-rpc/pdu/v3.5.0/peripherals.html
#   https://docs.python.org/3.7/howto/argparse.html
#   https://docs.python.org/3.7/library/argparse.html#module-argparse
#   https://avtech.com/articles/4957/updated-look-recommended-data-center-temperature-humidity/
#

#############################################################################

#
# imports
#

import sys
import os
import argparse

import raritan.rpc.peripheral
import raritan.rpc.sensors

#############################################################################

DEFAULT_ADMIN_USERNAME     = 'admin'
DEFAULT_ENVVAR_NAME        = 'PW'

#############################################################################

def settempthresholds(pdm, templist):
    global progname

    slots = pdm.getDeviceSlots()

    for num, slot in enumerate(slots):
        device = slot.getDevice()

        if device == None:
            print('Slot {} is empty'.format(num+1))
        elif device.deviceID.type.type != raritan.rpc.sensors.Sensor.TEMPERATURE:
            print('Slot {} is not a temperature sensor'.format(num+1))
        else:
            print('Setting thresholds on temperature sensor in slot {}'.format(num+1))

            settings = slot.getSettings()
            settings.useDefaultThresholds = False
            slot.setSettings(settings)

            thresholds = device.device.getThresholds()
            thresholds.lowerCritical = float(templist[0])
            thresholds.lowerWarning  = float(templist[1])
            thresholds.upperWarning  = float(templist[2])
            thresholds.upperCritical = float(templist[3])
            rc = device.device.setThresholds(thresholds)

            ### print(rc)

            if rc == 0:
                pass
            elif rc == raritan.rpc.sensors.NumericSensor.THRESHOLD_OUT_OF_RANGE:
                print('{}: cannot set thresholds on slot {} - threshold out of range'.format(progname, num+1))
                sys.exit(1)
            elif rc == raritan.rpc.sensors.NumericSensor.THRESHOLD_INVALID:
                print('{}: cannot set thresholds on slot {} - threshold invalid'.format(progname, num+1))
                sys.exit(1)
            elif rc == raritan.rpc.sensors.NumericSensor.THRESHOLD_NOT_SUPPORTED:
                print('{}: cannot set thresholds on slot {} - threshold not supported'.format(progname, num+1))
                sys.exit(1)
            else:
                print('{}: cannot set thresholds on slot {} - error code is {}'.format(progname, num+1, rc))
                sys.exit(1)

    return

#############################################################################

def main():
    global progname

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--host',   help='Raritan PDU hostname / IP address', required=True)
    parser.add_argument('--user',   help='default admin user name', default=DEFAULT_ADMIN_USERNAME)
    parser.add_argument('--envvar', help='environment variable name containing admin user password', default=DEFAULT_ENVVAR_NAME)
    parser.add_argument('--temps',   help='temperature thresholds (e.g. 10,15,30,35)', required=True)

    args = parser.parse_args()

    host = args.host

    username = args.user

    passwordvar = args.envvar

    try:
        password = os.environ[passwordvar]
    except KeyError:
        print('{}: password environment variable "{}" is not defined'.format(progname, passwordvar), file=sys.stderr)
        sys.exit(1)

    if password == '':
        print('{}: password environment variable "{}" is the null (empty) string'.format(progname, passwordvar), file=sys.stderr)
        sys.exit(1)

    temps = args.temps

    templist = temps.split(',')

    if len(templist) != 4:
        print('{}: --temps argument must be a list of 4 numbers seperated by commas'.format(progname), file=sys.stderr)
        sys.exit(1)

    for temp in templist:
        try:
            f = float(temp)
        except ValueError:
            print('{}: one of the temperature threshold numbers is badly formed'.format(progname), file=sys.stderr)
            sys.exit(1)
            

    agent = raritan.rpc.Agent('https', host, username, password, disable_certificate_verification=True, timeout=5)

    pdm = raritan.rpc.peripheral.DeviceManager("/model/peripheraldevicemanager", agent);

    try:
        settempthresholds(pdm, templist)
    except KeyboardInterrupt:
        print('', file=sys.stderr)
        print('*** interrupted by user typing Control^C ***', file=sys.stderr)

    return 0

#############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file

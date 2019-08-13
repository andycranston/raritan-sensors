#! /usr/bin/python3
#
# @(!==#) @(#) movesensorslot.py, version 005, 07-august-2019
#
# move a sensor from one slot to another (free) slot
#
#
# Links:
#
#   https://help.raritan.com/json-rpc/pdu/v3.5.0/index.html
#   https://help.raritan.com/json-rpc/pdu/v3.5.0/peripherals.html
#   https://docs.python.org/3.7/howto/argparse.html
#   https://docs.python.org/3.7/library/argparse.html#module-argparse
#

#############################################################################

#
# imports
#

import sys
import os
import argparse

import raritan.rpc.peripheral

#############################################################################

DEFAULT_ADMIN_USERNAME     = 'admin'
DEFAULT_ENVVAR_NAME        = 'PW'

#############################################################################

def showsensorslots(pdm):
    slots = pdm.getDeviceSlots()

    numslots = len(slots)

    print('PDU has {} sensor slots'.format(numslots))

    for num, slot in enumerate(slots, 1):
        device = slot.getDevice()
        ### print(device)

        if device == None:
            print('{:03d}: unassigned'.format(num))
        else:
            print('{:03d}: {} - {}'.format(num, settings.name, device.deviceID.serial))

            settings = slot.getSettings()
            ### print(settings)

            if device.deviceID.type.readingtype == raritan.rpc.sensors.Sensor.NUMERIC:
                reading = device.device.getReading()
                print("    Reading:", reading.value)
            else:
                state = device.device.getState()
                print("    State:", state.value)

    return

#############################################################################

def finddevice(discovereddevices, sourcedevice):
    found = None

    for i, discovered in enumerate(discovereddevices):
        ### print(i)
        ### print(discovered)

        if discovered.deviceID.serial != sourcedevice.deviceID.serial:
            continue

        if discovered.deviceID.type.readingtype != sourcedevice.deviceID.type.readingtype:
            continue

        if discovered.deviceID.type.type != sourcedevice.deviceID.type.type:
            continue

        if discovered.deviceID.type.unit != sourcedevice.deviceID.type.unit:
            continue

        found = i
        break

    return found

#############################################################################

def movesensorslot(pdm, sourceslot, destinationslot):
    global progname

    if sourceslot == destinationslot:
        print('{}: source slot {} and destination slot {} are the same'.format(progname, sourceslot, destinationslot), file=sys.stderr)
        sys.exit(1)

    if sourceslot < 1:
        print('{}: source slot {} is less than one'.format(progname, sourceslot), file=sys.stderr)
        sys.exit(1)

    if destinationslot < 1:
        print('{}: destination slot {} is less than one'.format(progname, destinationslot), file=sys.stderr)
        sys.exit(1)

    print('getting sensor slot info')

    slots = pdm.getDeviceSlots()

    numslots = len(slots)
    
    print('PDU has a total of {} sensor slots'.format(numslots))

    if sourceslot > numslots:
        print('{}: source slot {} is greater than {} which is the number of slots on the PDU'.format(progname, sourceslot, numslots), file=sys.stderr)
        sys.exit(1)

    if destinationslot > numslots:
        print('{}: destination slot {} is greater than {} which is the number of slots on the PDU'.format(progname, destinationslot, numslots), file=sys.stderr)
        sys.exit(1)

    print('getting sensor info from source slot {}'.format(sourceslot))

    sourcedevice = slots[sourceslot-1].getDevice()

    if sourcedevice == None:
        print('{}: source slot {} does not have a sensor in it'.format(progname, sourceslot), file=sys.stderr)
        sys.exit(1)

    print('checking destination slot {} is empty'.format(destinationslot))

    destinationdevice = slots[destinationslot-1].getDevice()

    if destinationdevice != None:
        print('{}: destination slot {} is already occupied with another sensor'.format(progname, destinationslot), file=sys.stderr)
        sys.exit(1)

    print('saving sensor settings')
    
    savesettings = slots[sourceslot-1].getSettings()

    ### print(sourcedevice)
    ### print(savesettings)

    ### deviceserial           = sourcedevice.deviceID.serial
    ### devicetypereadingtype  = sourcedevice.deviceID.type.readingtype
    ### devicetypetype         = sourcedevice.deviceID.type.type
    ### devicetypeunit         = sourcedevice.deviceID.type.unit

    ### print(deviceserial)
    ### print(devicetypereadingtype)
    ### print(devicetypetype)
    ### print(devicetypeunit)

    print('unassigning sensor slot {}'.format(sourceslot))
    slots[sourceslot-1].unassign()

    print('releasing sensor device')
    discovereddevices = pdm.getDiscoveredDevices()

    justunassigned = finddevice(discovereddevices, sourcedevice)

    if justunassigned == None:
        print('{}: FATAL ERROR! Cannot find the sensor just deleted from slot {}'.format(progname, sourceslot), file=sys.stderr)
        sys.exit(1)

    print('reassigning sensor to destination slot {}'.format(destinationslot))

    slots[destinationslot-1].assign(discovereddevices[justunassigned].deviceID)

    print('restoring saved settings to sensor slot {}'.format(destinationslot))

    slots[destinationslot-1].setSettings(savesettings)

    print('done')

    return

#############################################################################

def main():
    global progname

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--host',   help='Raritan PDU hostname / IP address', required=True)
    parser.add_argument('--user',   help='default admin user name', default=DEFAULT_ADMIN_USERNAME)
    parser.add_argument('--envvar', help='environment variable name containing admin user password', default=DEFAULT_ENVVAR_NAME)
    parser.add_argument('source_slot', help='sensor slot to move')
    parser.add_argument('destination_slot', help='new slot position for sensor')

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

    try:
        sourceslot = int(args.source_slot)
    except ValueError:
        print('{}: source slot {} is not an integer value'.format(progname, args.source_slot), file=sys.stderr)
        sys.exit(1)
    
    try:
        destinationslot = int(args.destination_slot)
    except ValueError:
        print('{}: destination slot {} is not an integer value'.format(progname, args.destination_slot), file=sys.stderr)
        sys.exit(1)
      
    agent = raritan.rpc.Agent('https', host, username, password, disable_certificate_verification=True, timeout=5)

    pdm = raritan.rpc.peripheral.DeviceManager("/model/peripheraldevicemanager", agent);

    # showsensorslots(pdm)

    movesensorslot(pdm, sourceslot, destinationslot)

    return 0

#############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file

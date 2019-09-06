#!/usr/bin/env python
import sys
import optparse
import time
import re
import serial
from serial import Serial





# Display a list of options to be sent to the plugin
def parse_args():
    parser = optparse.OptionParser()

    # Warning and Critical options
    parser.add_option(  "-w","--warning",
                        default=None,
                        type="int",
                        help="Warning value to be passed for the check.")
    parser.add_option(  "-c","--critical",
                        default=None,
                        type="int",
                        help="Critical value to be passed for the check.")
    parser.add_option(  "-p","--port",
                        default='/dev/ttyUSB0',
                        help="Port for device. defaults to /dev/ttyUSB0.")

    options, args = parser.parse_args()

    # Verify options are set
    if not options.warning:
        parser.error("Thresholds required for use. Use --help for more info.")
    if not options.critical:
        parser.error("Thresholds required for use. Use --help for more info.")

    return options

def main (options):
    warning = options.warning
    critical = options.critical
    port = options.port
    #try to open and read the serial port
    try:
        serialPort = serial.Serial(port)
        serialPort.write('TF\r')
        time.sleep(1)
        serData = ''
        serData += serialPort.read(1)
        serialPort.close()
    except FileNotFoundError:
        print ("ERROR: Unable to read sensor")
        sys.exit(3)
    #if it returns nothing exit with unknown
    if (serData == ''):
        print ("ERROR: Unable to read sensor")
        sys.exit(3)
    #regex to get the number
    temp = re.findall("[\d]+.[\d]+",serData)

    exitcode = 3
    #set the exit code based on reading
    if (temp > warning):
        exitcode = 1
        print ("WARNING: Temp is at %s F" % temp)
    if (temp > critical):
        exitcode = 2
        print ("CRITICAL: Temp is at %s F" % temp)
    if (temp < warning):
        exitcode = 0
        print ("OK: Temp is at %s F" % temp)
    #exit
    sys.exit(exitcode)
    
#call the things
options = parse_args()
main(options)
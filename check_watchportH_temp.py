#!/usr/bin/env python
#	check_watchportT.py
# 	Copyright 2019 Nathan Safran
#
#	This script gets the temperature from a Digi Watchport Temperature Sensor.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
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
        serialPort = serial.Serial(port, timeout=2)
        serialPort.write('TF\r')
        time.sleep(1)
        serData = ''
        serData += serialPort.read_until()
        serialPort.close()
    except IOError:
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
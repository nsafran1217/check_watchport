#!/usr/bin/env python
#	check_watchportT_humid.py
# 	Copyright 2019 Nathan Safran
#
#	This script gets the humidityfrom a Digi Watchport/H Sensor.
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
import re
import serial
from serial import Serial
from usb.core import find as finddev


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
    dev = finddev(idVendor=0x1608, idProduct=0x0305)
    warning = options.warning
    critical = options.critical
    port = options.port
    #try to open and read the serial port
    try:
        serialPort = serial.Serial(port, timeout=2)
        serialPort.write('H\r')
        serData = ''
        serData += serialPort.read_until()
        serialPort.close()
    except IOError:
        print ("ERROR: Unable to read sensor. Is the port correct?")
        dev.reset()
        sys.exit(3)
    #if it returns nothing exit with unknown
    if (serData == ''):
        print ("ERROR: Unable to read sensor. Is the port correct?")
        dev.reset()
        sys.exit(3)
    #regex to get the number
    humidity = int((re.search("[\d]+",serData)).group(0))

    exitcode = 3
    #set the exit code based on reading
    if (humidity >= warning and humidity < critical):
        exitcode = 1
        print ("WARNING:  Humidity is at %s %%" % humidity)
    if (humidity >= critical):
        exitcode = 2
        print ("CRITICAL: Humidity is at %s %%" % humidity)
    if (humidity < warning):
        exitcode = 0
        print ("OK: Humidity is at %s %%" % humidity)
    #exit
  
    dev.reset()
    #Perfomance Data
    print "|humidity=%s;%s;%s;0;100\n" % (humidity,warning,critical)
    sys.exit(exitcode)
    
#call the things
options = parse_args()
main(options)
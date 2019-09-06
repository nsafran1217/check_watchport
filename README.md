# check_watchportT
Nagios plugin for checking temperature from a watchport sensor
add the nagios user to the dailout group so it has access to the serial port
Important to consider:
I wrote this because the sensor I'm using would need reset after every read. You may not have this issue. 
You should comment out the lines about the usb device.
If you need to reset your device, change the device id in the script. also you need to set the permissions on the device with a udev rule.
GL

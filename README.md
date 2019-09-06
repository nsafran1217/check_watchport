# check_watchportT
Nagios plugin for checking temperature from a watchport sensor.

Add the nagios user to the dailout group so it has access to the serial port.

The normal version should work without modification

# USB version:
I had a lot of problems with the sensor locking after every read. I wrote the USB versions to reset the device after every check.
If you want to use this version, you will have to change the device IDs to match. I also had to use a udev rule to set an acl on the device to allow the nagios user rw access to it. An example is included.

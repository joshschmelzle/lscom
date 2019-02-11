# -*- coding: utf-8 -*-

"""
list active com ports
~~~~~~~~~~~~~~~~~~~~~

make sure you have the pyserial package installed.
"""

import sys
import glob

try:
    import serial
except ModuleNotFoundError:
    print("required module pyserial not found... exiting...")
    sys.exit(-1)


def list_active_serial_port_names():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            _serial = serial.Serial(port)
            _serial.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == "__main__":
    print(list_active_serial_port_names())

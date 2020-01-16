# -*- coding: utf-8 -*-

"""
list active com ports
~~~~~~~~~~~~~~~~~~~~~

make sure you have the pyserial package installed.
"""

from .lscom import list_active_serial_port_names


def main():
    """Get and list available serial port names"""
    print(list_active_serial_port_names())


if __name__ == "__main__":
    main()

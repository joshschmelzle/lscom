# -*- coding: utf-8 -*-
#
# |  _  _  _  ._ _
# | _> (_ (_) | | |

"""
lscom 
~~~~~

list available serial ports
"""

from .lscom import list_active_serial_port_names


def main():
    """Get and list available serial port names"""
    print(list_active_serial_port_names())


if __name__ == "__main__":
    main()

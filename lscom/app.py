# -*- coding: utf-8 -*-

# |  _  _  _  ._ _
# | _> (_ (_) | | |

"""
lscom.app
~~~~~~~~~

main app code
"""

import glob
import grp
import os
import sys

try:
    import serial  # type: ignore
except ModuleNotFoundError:
    print("required module pyserial not found... exiting...")
    sys.exit(-1)


class lscom:
    """Main application class."""

    def check_serial_permissions(self):
        """
        Check if current user has permissions for serial port access on Linux.

        Add to dialout:
            sudo usermod -a -G dialout $USER

        Remove from dialout:
            sudo gpasswd -d $USER dialout

        :returns:
            Tuple: (bool, message)
        """
        if not sys.platform.startswith("linux"):
            return True, "Permission check required"

        try:
            dialout = grp.getgrnam("dialout")
            groups = os.getgroups()
            user = os.getlogin()
            if dialout.gr_gid in groups:
                return True, f"{user} has dialout group access"
            else:
                return (
                    False,
                    f"""
    {user} is not in the dialout group. To fix:
    1. Run: sudo usermod -a -G dialout {user}
    2. Log out and back in for the changes to take effect
    """,
                )
        except KeyError:
            return False, "dialout group not found"
        except Exception as error:
            return False, f"Error checking permissions: {str(error)}"

    def get_active_serial_port_names(self):
        """Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        has_permissions, message = self.check_serial_permissions()
        if not has_permissions:
            print(message)
        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError(
                "appears to be an unsupported platform", sys.platform
            )

        result = []
        for port in ports:
            try:
                _serial = serial.Serial(port)
                _serial.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def run(self):
        serials = self.get_active_serial_port_names()
        if len(serials) > 0:
            print("{0} serial ports detected and available:".format(len(serials)))
            for _ in serials:
                print(_)
        else:
            print("no available serial ports detected")


def run() -> None:
    """Run the application."""
    lscom().run()

# -*- coding: utf-8 -*-

# |  _  _  _  ._ _
# | _> (_ (_) | | |

"""
lscom.app
~~~~~~~~~

main app code
"""

import glob
import os
import subprocess
import sys

try:
    import serial  # type: ignore
except ModuleNotFoundError:
    print("required module pyserial not found... exiting...")
    sys.exit(-1)

try:
    import termios  # POSIX only
except ImportError:
    termios = None  # type: ignore


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
            import grp

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
    2. Run: newgrp dialout (to apply changes immediately)
       Or log out and back in for the changes to take effect
    """,
                )
        except KeyError:
            return False, "dialout group not found"
        except Exception as error:
            return False, f"Error checking permissions: {str(error)}"

    def get_active_serial_port_names(self):
        """Lists serial port names that exist and are not currently in use.

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        has_permissions, message = self.check_serial_permissions()
        if not has_permissions:
            print(message)
        ports = self._discover_ports()
        busy = self._busy_ports(ports)
        return [p for p in ports if p not in busy and self._is_real_tty(p)]

    def _discover_ports(self):
        """Return all candidate serial-port paths for the current platform."""
        if sys.platform.startswith("win"):
            return ["COM%s" % (i + 1) for i in range(256)]
        if sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            return glob.glob("/dev/tty[A-Za-z]*")
        if sys.platform.startswith("darwin"):
            # macOS exposes each serial device twice: /dev/tty.<name> (callin)
            # and /dev/cu.<name> (callout). The tty.* node engages modem-control
            # / carrier-detect semantics that cause tcsetattr() to fail with
            # EINVAL on USB serial adapters when no carrier is present.
            # Prefer cu.*, fall back to tty.* only if no cu.* peer.
            cu_ports = glob.glob("/dev/cu.*")
            cu_suffixes = {os.path.basename(p)[3:] for p in cu_ports}  # strip "cu."
            return cu_ports + [
                p
                for p in glob.glob("/dev/tty.*")
                if os.path.basename(p)[4:] not in cu_suffixes
            ]
        raise EnvironmentError("appears to be an unsupported platform", sys.platform)

    def _busy_ports(self, ports):
        """Return the set of port paths currently held open by any process.

        Uses `lsof` because most serial applications (SecureCRT, terminal
        emulators, etc.) hold the device open without any advisory lock,
        so flock/TIOCEXCL probes can't detect them. Returns an empty set
        on systems where lsof isn't available or the call fails.
        """
        if not ports or sys.platform.startswith("win"):
            return set()
        try:
            proc = subprocess.run(
                ["lsof", "-F", "n", "--", *ports],
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return set()
        # lsof exits 1 when no listed file is open; that's not an error here.
        # Output lines beginning with 'n' are file paths.
        port_set = set(ports)
        return {
            line[1:]
            for line in proc.stdout.splitlines()
            if line.startswith("n") and line[1:] in port_set
        }

    def _is_real_tty(self, port):
        """Return True if `port` is a real, openable serial-style device.

        On POSIX we avoid pyserial's full open(), which calls
        tcsetattr() and fails with EINVAL on some macOS USB-serial drivers
        (e.g. CH340) even for usable devices. A raw non-blocking
        open + tcgetattr is sufficient to confirm the device is a tty.
        """
        if sys.platform.startswith("win"):
            try:
                serial.Serial(port).close()
                return True
            except Exception:
                return False
        try:
            fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        except OSError as error:
            print(f"skipping {port}: {error}", file=sys.stderr)
            return False
        try:
            termios.tcgetattr(fd)  # type: ignore
            return True
        except Exception as error:
            print(f"skipping {port}: {error}", file=sys.stderr)
            return False
        finally:
            try:
                os.close(fd)
            except OSError:
                pass

    def run(self):
        serials = self.get_active_serial_port_names()
        if serials:
            print(f"{len(serials)} serial ports detected and available:")
            for port in serials:
                print(port)
        else:
            print("no available serial ports detected")


def run() -> None:
    """Run the application."""
    lscom().run()

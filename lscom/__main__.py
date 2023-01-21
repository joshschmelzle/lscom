# -*- coding: utf-8 -*-

# |  _  _  _  ._ _
# | _> (_ (_) | | |

"""
lscom
~~~~~

list available serial ports
"""

import sys

from lscom import helpers
from lscom.__version__ import __title__, __version__
from lscom.app import run

PY_MAJOR = 3
PY_MINOR = 2
MINIMUM_PYTHON_VERISON = "3.2"


def check_python_version():  # type: ignore
    """Use old-school .format() method for if someone uses with very old Python."""
    msg = """

{title} version {pkgv} requires Python version {pyv} or higher.
""".format(
        title=__title__, pkgv=__version__, pyv=MINIMUM_PYTHON_VERISON
    )
    if sys.version_info < (PY_MAJOR, PY_MINOR):
        raise ValueError(msg)


def main():
    parser = helpers.setup_parser()
    args = parser.parse_args()  # noqa: F841
    run()


def init():
    check_python_version()  # type: ignore

    if __name__ == "__main__":
        main()
        sys.exit(0)


init()

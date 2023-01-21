# -*- coding: utf-8 -*-

# |  _  _  _  ._ _
# | _> (_ (_) | | |

"""
lscom.helpers
~~~~~~~~~~~~~

helper functions
"""

import argparse

from lscom.__version__ import __version__


def setup_parser():
    """Set default values and handle arg parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="lscom: list and discover available COM ports",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"lscom version is {__version__}"
    )
    return parser

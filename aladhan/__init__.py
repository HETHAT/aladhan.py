"""
Aladhan prayer times API Wrapper
~~~~~~~~~~~~~~~~~~~~~
Basic wrapper for the Aladhan prayer times API.
"""

from collections import namedtuple

VersionInfo = namedtuple(
    "VersionInfo", "major minor micro releaselevel serial"
)

version_info = VersionInfo(
    major=1, minor=2, micro=0, releaselevel="alpha", serial=0
)

__title__ = "aladhan.py"
__author__ = "HETHAT"
__version__ = "1.2.0a"


from .client import Client
from .data_classes import *
from . import methods
from .methods import Method
from .enums import *

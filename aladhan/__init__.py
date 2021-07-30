"""
Aladhan prayer times API Wrapper
~~~~~~~~~~~~~~~~~~~~~
Basic wrapper for the Aladhan prayer times API.
"""

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(
    major=1, minor=0, micro=0, releaselevel="", serial=0
)

__title__ = "aladhan.py"
__author__ = "HETHAT"
__version__ = "1.0.0"


from .client import Client
from .base_types import *
from . import methods
from .methods import Method
from .enums import *

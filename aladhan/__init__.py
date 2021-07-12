"""
Aladhan prayer times API Wrapper
~~~~~~~~~~~~~~~~~~~~~
Basic async wrapper for the Aladhan prayer times API.
"""

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(
    major=0, minor=3, micro=0, releaselevel="alpha", serial=0
)

__title__ = "aladhan.py"
__author__ = "HETHAT"
__version__ = "0.3.0a"


from .client import AsyncClient
from .base_types import *
from . import methods
from .methods import Method
from .enums import *

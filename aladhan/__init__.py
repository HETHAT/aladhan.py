"""
Aladhan prayer times API Wrapper
~~~~~~~~~~~~~~~~~~~~~
Basic async wrapper for the Aladhan prayer times API.
"""

from typing import NamedTuple

VersionInfo = NamedTuple(
    "VersionInfo", major=int, minor=int, micro=int, releaselevel=str, serial=int
)

version_info = VersionInfo(major=0, minor=1, micro=4, releaselevel="", serial=0)

__title__ = "aladhan.py"
__author__ = "HETHAT"
__version__ = "0.1.4"


from .client import AsyncClient
from .base_types import *
from .endpoints import EndPoints
from . import methods

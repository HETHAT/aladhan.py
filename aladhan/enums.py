from enum import Enum

__all__ = ("Schools", "MidnightModes", "LatitudeAdjustmentMethods")


class Schools(Enum):
    """Available schools"""

    STANDARD = SHAFI = 0
    HANAFI = 1


class MidnightModes(Enum):
    """Available midnight modes"""

    STANDARD = 0
    JAFARI = 1


class LatitudeAdjustmentMethods(Enum):
    """Available latitude adjustment methods"""

    MIDDLE_OF_THE_NIGHT = 1
    ONE_SEVENTH = 2
    ANGLE_BASED = 3

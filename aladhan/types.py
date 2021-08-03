from typing import List, Dict, Union

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

__all__ = (
    "AsmaRes",
    "CalendarRes",
    "Date",
    "MonthCalendarRes",
    "QiblaRes",
    "TimingsRes",
    "YearCalendarRes",
    "DateToCalendarRes",
    "DateToDateRes",
)


class _Timings(TypedDict):
    Fajr: str
    Sunrise: str
    Dhuhr: str
    Asr: str
    Sunset: str
    Maghrib: str
    Isha: str
    Imsak: str
    Midnight: str


class _WeekdayOptional(TypedDict, total=False):
    ar: str


class _Weekday(_WeekdayOptional):
    en: str


class _Month(_Weekday):
    number: int


class _Designation(TypedDict):
    abbreviated: str
    expanded: str


class _DateTypeOptional(TypedDict, total=False):
    holidays: List[str]


class _DateType(_DateTypeOptional):
    date: str
    format: str
    day: str
    weekday: _Weekday
    month: _Month
    year: str
    designation: _Designation


class _DateOptional(TypedDict, total=False):
    readable: str
    timestamp: str


class Date(_DateOptional):
    gregorian: _DateType
    hijri: _DateType


class _MethodParams(TypedDict, total=False):
    Fajr: int
    Maghrib: int
    Isha: int


class _Method(TypedDict):
    id: Literal[0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    name: str
    params: _MethodParams


class _Offset(TypedDict):
    Fajr: int
    Sunrise: int
    Dhuhr: int
    Asr: int
    Sunset: int
    Maghrib: int
    Isha: int
    Imsak: int
    Midnight: int


class _Meta(TypedDict):
    longitude: float
    latitude: float
    timezone: str
    method: _Method
    latitudeAdjustmentMethod: Literal[
        "MIDDLE_OF_THE_NIGHT", "ONE_SEVENTH", "ANGLE_BASED"
    ]
    midnightMode: Literal["STANDARD", "JAFARI"]
    school: Literal["STANDARD", "HANAFI"]
    offset: _Offset


class TimingsRes(TypedDict):
    timings: _Timings
    date: Date
    meta: _Meta


class QiblaRes(TypedDict):
    latitude: float
    longitude: float
    direction: float


class _IsmEn(TypedDict):
    meaning: str


class _Ism(TypedDict):
    name: str
    transliteration: str
    number: int
    en: _IsmEn


AsmaRes = List[_Ism]
MonthCalendarRes = List[TimingsRes]
YearCalendarRes = Dict[
    Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    MonthCalendarRes,
]
CalendarRes = Union[MonthCalendarRes, YearCalendarRes]
DateToCalendarRes = List[Date]
DateToDateRes = Date

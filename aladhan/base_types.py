import pytz

from datetime import datetime, timedelta
from typing import Dict, Union, List
from functools import partial
from beartype import beartype

from .methods import all_methods, Method, ISNA

__all__ = (
    "Data",
    "Date",
    "DateType",
    "Meta",
    "LatitudeAdjustmentMethods",
    "MidnightModes",
    "Timings",
    "Tune",
    "Prayer",
    "Schools",
    "TimingsDateArg",
    "CalendarDateArg",
    "DefaultArgs",
)


class Tune:
    def __init__(
        self,
        Imsak: int = 0,
        Fajr: int = 0,
        Sunrise: int = 0,
        Dhuhr: int = 0,
        Asr: int = 0,
        Maghrib: int = 0,
        Sunset: int = 0,
        Isha: int = 0,
        Midnight: int = 0,
    ):
        self.imsak = Imsak
        self.fajr = Fajr
        self.sunrise = Sunrise
        self.dhuhr = Dhuhr
        self.asr = Asr
        self.maghrib = Maghrib
        self.sunset = Sunset
        self.isha = Isha
        self.midnight = Midnight

    @property
    def value(self):
        return (
            "{0.imsak},{0.fajr},{0.sunrise},{0.dhuhr},{0.asr},"
            "{0.maghrib},{0.sunset},{0.isha},{0.midnight}".format(self)
        )

    @classmethod
    def from_str(cls, s: str) -> "Tune":
        args = s.split(",")
        assert len(args) == 9, "Not valid string format"
        return cls(*map(int, args))

    def __str__(self):
        return "<Tune = {}>".format(self.value)


class Schools:
    STANDARD = SHAFI = 0
    HANAFI = 1


class MidnightModes:
    STANDARD = 0
    JAFARI = 1


class LatitudeAdjustmentMethods:
    MIDDLE_OF_THE_NIGHT = 1
    ONE_SEVENTH = 2
    ANGLE_BASED = 3


class Prayer:
    def __init__(self, name: str, time: str, date: str = None):
        self.name = name
        if date is None:
            date = datetime.utcnow().strftime("%d-%m-%Y")
        day, month, year = map(int, date.split("-"))
        time = time.split()[0]
        self.time = datetime.strptime(time, "%H:%M").replace(year, month, day)
        self.str_time = self.time.strftime("%H:%M %d-%m-%Y")

    def remaining(self):
        return self.time - datetime.utcnow()

    def __str__(self):
        return "<Prayer name={0.name!r}, time=D{0.str_time!r}>".format(self)

    def __repr__(self):
        return "<Prayer object>"


class CalendarDateArg:
    @beartype
    def __init__(
        self,
        year: int,
        month: int = None,
        hijri: bool = False,
    ):
        """
        :param year: required argument for calendar's year
        :param month: if this was not giving, or 0 was giving instead it will return a whole year calendar instead
         which is set to by default
        :param hijri: if the year that is given either a hijri year or not, set to False by default
        """
        # TODO: check for year limits
        if month:
            if month not in range(1, 13):
                raise ValueError(
                    "month argument expected to be in range 1-12"
                    " got {}".format(month)
                )
            self.month = month
            self.annual = "false"
        else:
            self.month = 0
            self.annual = "true"

        self.year = year
        self.hijri = hijri

    @property
    def as_dict(self):
        return {"year": self.year, "annual": self.annual, "month": self.month}


class TimingsDateArg:
    @beartype
    def __init__(self, date: Union[str, int, datetime] = None):
        """
        :param date: can either a string representing a DD-MM-YYYY date format or an integer representing a unix
         timestamp or datetime obj, set to current utc date by default
        """
        if date is None:
            date = datetime.utcnow()
        elif isinstance(date, int):
            date = datetime.utcfromtimestamp(date)

        if isinstance(date, datetime):
            date = date.strftime("%d-%m-%Y")

        else:  # it is a str
            try:
                datetime.strptime(date, "%d-%m-%Y")
            except ValueError:
                raise ValueError(
                    "Expected DD-MM-YYYY date format got {!r} ".format(date)
                )

        self.date = date  # noqa


class DefaultArgs:
    @beartype
    def __init__(
        self,
        method: Union[Method, int] = ISNA,
        tune: Tune = None,
        school: int = Schools.SHAFI,
        midnightMode: int = MidnightModes.STANDARD,  # noqa
        latitudeAdjustmentMethod: int = LatitudeAdjustmentMethods.ANGLE_BASED,  # noqa
        adjustment: int = 0,
    ):
        """
        every getter has this arguments so instead of repeating it and its checking
        this is used which saved a lot of code.

        :param method: a prayer time calculation method, you can look into all
        methods from methods.all_methods, set to "Islamic Society of North America"
        by default
        :param tune: to offset returned timings set to empty Tune() by default
        :param school: 0 for Shafi (standard), 1 for Hanafi, defaults to Shafi
        :param midnightMode: 0 for Standard (Mid Sunset to Sunrise),
        1 for Jafari (Mid Sunset to Fajr), defaults to Standard
        :param latitudeAdjustmentMethod: Method for adjusting times higher latitudes.
        For instance, if you are checking timings in the UK or Sweden.
        1 - Middle of the Night
        2 - One Seventh
        3 - Angle Based
        default to Angle Based
        :param adjustment: Number of days to adjust hijri date(s)
        """
        # method
        if isinstance(method, Method):
            method = method.id

        if method not in range(16):
            raise ValueError("Expected method in 0-15 range" " got {!r}".format(method))
        self.method = method

        # tune
        if tune is None:
            tune = Tune().value
        elif isinstance(tune, Tune):
            tune = tune.value
        self.tune = tune

        # school
        if school not in (0, 1):
            raise ValueError(
                "School argument can only be either 0 or 1" " got {!r}".format(school)
            )
        self.school = school

        # midnight mode
        if midnightMode not in (0, 1):
            raise ValueError(
                "midnightMode argument can only be either 0 or 1"
                " got {!r}".format(midnightMode)
            )
        self.midnightMode = midnightMode

        # lat adj methods
        if latitudeAdjustmentMethod not in (1, 2, 3):
            raise ValueError(
                "latitudeAdjustmentMethod argument can only be either 1, 2 or 3"
                " got {!r}".format(latitudeAdjustmentMethod)
            )
        self.latitudeAdjustmentMethod = latitudeAdjustmentMethod

        self.adjustment = adjustment

    @property
    def as_dict(self):
        return {
            "method": self.method,
            "tune": self.tune,
            "school": self.school,
            "midnightMode": self.midnightMode,
            "latitudeAdjustmentMethod": self.latitudeAdjustmentMethod,
            "adjustment": self.adjustment,
        }


class Meta:
    def __init__(
        self,
        data: "Data",
        longitude: float,
        latitude: float,
        timezone: str,
        method: dict,
        latitudeAdjustmentMethod: str,
        midnightMode: str,
        school: str,
        offset: dict,
    ):
        self.data = data
        self.longitude = longitude
        self.latitude = latitude
        self.timezone = pytz.timezone(timezone)
        self.method = all_methods[method["id"]]
        self.latitudeAdjustmentMethod = latitudeAdjustmentMethod
        self.midnightMode = midnightMode
        self.school = school
        self.offset = Tune(*offset)

    def __str__(self):
        return (
            "<Meta longitude={0.longitude!r}, latitude={0.latitude!r}, "
            "method={0.method!r}, latitudeAdjustmentMethod={0.latitudeAdjustmentMethod!r}, "
            "midnightMode={0.midnightMode!r}, school={0.school!r}, offset={0.offset!r}>"
        )

    def __repr__(self):
        return "<Meta object>"

    @property
    def default_args(self):
        return DefaultArgs(
            self.method,
            self.offset,
            getattr(Schools, self.school.upper()),
            getattr(MidnightModes, self.midnightMode.upper()),
            getattr(LatitudeAdjustmentMethods, self.latitudeAdjustmentMethod.upper())
            # can't get adjustment ...
        )


class DateType:
    def __init__(
        self,
        name: str,
        date: str,
        format: str,  # noqa
        day: str,
        weekday: Dict[str, str],
        month: Dict[str, Union[int, str]],
        year: str,
        designation: Dict[str, str],
        holidays: List[str] = None,
    ):
        self.name = name
        self.date = date
        self.format = format
        self.day = int(day)
        self.weekday = weekday
        self.month = month
        self.year = int(year)
        self.designation = designation
        self.holidays = holidays

    def __str__(self):
        return (
            "<DateType name={0.name!r}, date={0.date!r}, holidays={0.holidays}>".format(
                self
            )
        )

    def __repr__(self):
        return "<DateType object>"


class Date:
    def __init__(
        self,
        data: "Data",
        readable: str,
        timestamp: str,
        gregorian: dict,
        hijri: dict,
    ):
        self.data = data
        self.readable = readable
        self.timestamp = int(timestamp)
        self.gregorian = DateType("Gregorian", **gregorian)
        self.hijri = DateType("Hijri", **hijri)

    def __str__(self):
        return (
            "<Date readable={0.readable!r}, timestamp={0.timestamp!r}, "
            "gregorian={0.gregorian!r}, hijri={0.hijri!r}>".format(self)
        )

    def __repr__(self):
        return "<Date object>"


class Timings:
    def __init__(
        self,
        data: "Data",
        Imsak: str,
        Fajr: str,
        Sunrise: str,
        Dhuhr: str,
        Asr: str,
        Maghrib: str,
        Sunset: str,
        Isha: str,
        Midnight: str,
    ):
        self.data = data
        _Prayer = partial(Prayer, date=data.date.gregorian.date)
        self.imsak: Prayer = _Prayer("Imsak", Imsak)
        self.fajr: Prayer = _Prayer("Fajr", Fajr)
        self.sunrise: Prayer = _Prayer("Sunrise", Sunrise)
        self.dhuhr: Prayer = _Prayer("Dhuhr", Dhuhr)
        self.asr: Prayer = _Prayer("Asr", Asr)
        self.sunset: Prayer = _Prayer("Sunset", Sunset)
        self.maghrib: Prayer = _Prayer("Maghrib", Maghrib)
        self.isha: Prayer = _Prayer("Isha", Isha)
        self.midnight: Prayer = _Prayer("Midnight", Midnight)

    @property
    def prayers_only(self):
        return {
            "Fajr": self.fajr,
            "Dhuhr": self.dhuhr,
            "Asr": self.asr,
            "Maghrib": self.maghrib,
            "Isha": self.isha,
        }

    async def next_prayer(self):
        meta = self.data.meta
        now = datetime.utcnow()
        now = now + meta.timezone.utcoffset(now)
        for key, val in self.prayers_only.items():
            if now < val.time:
                return val

        return await (
            await self.data.client.get_timings(
                meta.longitude,
                meta.latitude,
                TimingsDateArg(
                    datetime(val.time.year, val.time.month, val.time.day)  # noqa
                    + timedelta(1)
                ),
                meta.default_args,
            )
        ).timings.next_prayer()

    def __str__(self):
        return (
            "<Timings imsak={0.imsak}, fajr={0.fajr}, sunrise={0.sunrise}, "
            "dhuhr={0.dhuhr}, asr={0.asr}, sunset={0.sunset}, maghrib={0.maghrib}, "
            "isha={0.isha}, midnight={0.midnight}>".format(self)
        )

    def __repr__(self):
        return "<Timings object>"


class Data:
    def __init__(self, timings: dict, date: dict, meta: dict, client):
        self.meta = Meta(self, **meta)
        self.date = Date(self, **date)
        self.timings = Timings(self, **timings)
        self.client = client

    def __str__(self):
        return "<Data meta={0.meta!r}, date={0.date!r}, timings={0.timings!r}>".format(
            self
        )

    def __repr__(self):
        return "<Data object | {0.gregorian.date}>".format(self.date)

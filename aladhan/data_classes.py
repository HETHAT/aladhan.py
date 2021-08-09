import pytz

from datetime import datetime
from typing import Dict, Union, List, Optional, Iterable
from functools import partial

from .methods import all_methods, Method, ISNA
from .exceptions import *
from .enums import *

__all__ = (
    "Data",
    "Date",
    "DateType",
    "Meta",
    "Timings",
    "Tune",
    "Prayer",
    "TimingsDateArg",
    "CalendarDateArg",
    "Parameters",
    "Qibla",
    "Ism",
    "Method",
)


class Tune:
    """
    Represents a Tune obj that is returned from API.
    Can be used to make an obj that will be used as a tune param in \
    :class:`Parameters`

    Attributes
    ----------
        imsak: :class:`int`
            The tune value for imsak.
        fajr: :class:`int`
            The tune value for fajr.
        sunrise: :class:`int`
            The tune value for sunrise.
        asr: :class:`int`
            The tune value for asr.
        maghrib: :class:`int`
            The tune value for maghrib.
        sunset: :class:`int`
            The tune value for sunset.
        isha: :class:`int`
            The tune value for isha.
        midnight: :class:`int`
            The tune value for midnight.

    *New in v1.0.: __iter__*
    """

    __slots__ = (
        "imsak",
        "fajr",
        "sunrise",
        "dhuhr",
        "asr",
        "maghrib",
        "sunset",
        "isha",
        "midnight",
    )

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
        """:class:`str`: The string value that will be used to
            get response.

        Format:
            imsak,fajr,sunrise,dhuhr,asr,maghrib,sunset,isha,midnight
        """
        return (
            "{0.imsak},{0.fajr},{0.sunrise},{0.dhuhr},{0.asr},"
            "{0.maghrib},{0.sunset},{0.isha},{0.midnight}".format(self)
        )

    @classmethod
    def from_str(cls, s: str) -> "Tune":
        """Makes a Tune obj from a value string.

        Returns
        -------
            :class:`Tune`
                The created obj.

        Raises
        ------
            :exc:`AsserationError`
                Invalid string format.
        """
        args = s.split(",")
        assert (
            len(args) == 9
        ), "Invalid string format, must be in Tune.value format."
        return cls(*map(int, args))

    def __iter__(self):  # pragma: no cover
        yield from map(int, self.value.split(","))

    def __repr__(self):  # pragma: no cover
        return "<Tune = {}>".format(self.value)

    def __hash__(self):  # pragma: no cover
        return hash(self.value)


class Qibla:
    """Represents a Qibla obj.

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        longitude: :class:`float`
            Longitude coordinate.
        latitude: :class:`float`
            Latitude coordinate.
        direction: :class:`float`
            Qibla direction.

    *New in v0.1.3*
    """

    __slots__ = ("longitude", "latitude", "direction")

    def __init__(self, longitude: float, latitude: float, direction: float):
        self.longitude = longitude
        self.latitude = latitude
        self.direction = direction

    def __repr__(self):  # pragma: no cover
        return "<Qibla longitude={0.longitude} latitude={0.latitude}>".format(
            self
        )

    def __hash__(self):  # pragma: no cover
        return hash((self.longitude, self.latitude, self.direction))


class Ism:
    """Represents an Ism obj.

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        name: :class:`str`
            The name in arabic.
        transliteration: :class:`str`
            The transliteration of the name.
        number: :class:`int`
            Ism's number/id.
        en: :class:`str`
            The name in english.

    *New in v0.1.3*
    """

    __slots__ = ("name", "transliteration", "number", "en")

    def __init__(self, name: str, transliteration: str, number: int, en: dict):
        self.name = name
        self.transliteration = transliteration
        self.number = number
        self.en = en["meaning"]

    def __repr__(self):  # pragma: no cover
        return "<Ism name={0.name} en={0.en}>".format(self)

    def __hash__(self):  # pragma: no cover
        return hash(self.name)


class Prayer:
    """Represents a Prayer obj.

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        timings: :class:`Timings`
            Original Timings obj.
        name: :class:`str`
            Prayer name.
        time: :class:`datetime.datetime`
            Prayer's time.
        time_utc: Optional[:class:`datetime.datetime`]
            Prayer's time in utc, might be None when time doesn't exist
            because of a daylight savings switch.
        str_time: :class:`str`
            Better looking string format for prayer's time.

    *New in v0.1.2: timings, time_utc*
    """

    __slots__ = ("timings", "name", "time", "time_utc", "str_time")

    def __init__(
        self, name: str, time: str, timings: "Timings", date: str = None
    ):
        self.timings = timings
        self.name = name
        if date is None:
            date = datetime.utcnow().strftime("%d-%m-%Y")
        day, month, year = map(int, date.split("-"))
        time = time.split()[0]
        self.time = datetime.strptime(time, "%H:%M").replace(year, month, day)
        try:
            self.time_utc = self.time + timings.data.meta.timezone.utcoffset(
                self.time
            )
        except pytz.exceptions.NonExistentTimeError:  # pragma: no cover
            self.time_utc = None
        self.str_time = self.time.strftime("%H:%M %d-%m-%Y")

    @property
    def remaining(self):
        """:class:`datetime.timedelta`: remaining time for prayer.

        *New in v0.1.2*
        """
        return self.time - datetime.utcnow()

    @property
    def remaining_utc(self):
        """Optional[:class:`datetime.timedelta`]:
         remaining time for prayer for utc.

        *New in v0.1.2*
        """
        return self.time_utc and self.time_utc - datetime.utcnow()

    def __repr__(self):  # pragma: no cover
        return "<Prayer name={0.name!r}, time=D{0.str_time!r}>".format(self)

    def __hash__(self):  # pragma: no cover
        return hash(self.name)


class CalendarDateArg:
    """
    Class to make an obj that will be used as a date param in calendar
        getters

    Parameters
    ----------
        year: :class:`int`
            Required argument for calendar's year.

        month: Optional[:class:`int`]
            If this was not giving, or 0 was giving instead it will
            return a whole year calendar instead which is set to by
            default

        hijri: :class:`bool`
            whether `year` is a hijri year or not.
            Default: False

    Attributes
    ----------
        year: :class:`int`
            Calendar's year.

        month: :class:`int`
            Calendar's month, set to 0 if it wasn't given.

        annual: :class:`str`
            Whether a year calender going to be returned ot not.
            "true" if month was not given otherwise "false".

        hijri: :class:`bool`
            Whether `year` given is a hijri year or not.

    Raises
    ------
        :exc:`ValueError`
            Month passed is not in 1-12 range.
    """

    __slots__ = ("year", "month", "hijri", "annual")

    def __init__(
        self,
        year: int,
        month: Optional[int] = None,
        hijri: bool = False,
    ):
        if month:
            if month not in range(1, 13):  # pragma: no cover
                raise ValueError(
                    "month argument expected to be in range 1-12"
                    " got {}".format(month)
                )
            self.month: int = month
            self.annual = "false"
        else:
            self.month: int = 0
            self.annual = "true"

        self.year = year
        self.hijri = hijri

    @property
    def as_dict(self):
        return {"year": self.year, "annual": self.annual, "month": self.month}

    def __hash__(self):  # pragma: no cover
        return hash((self.year, self.annual, self.month))


class TimingsDateArg:
    """
    Class to make an obj that will be used as a date param in timings getters

    Parameters
    ----------
        date: Optional[:class:`int` or :class:`str`
            or :class:`datetime.datetime`]

            Can be either int representing the UNIX format or a str in
            DD-MM-YYYY format or a datetime obj.
            Default: current date.

    Attributes
    ----------
        date: :class:`str`
            A date string in DD-MM-YYYY format.

    Raises
    ------
        :exc:`AsserationError`
            Invalid date string format.
    """

    __slots__ = "date"

    def __init__(self, date: Optional[Union[str, int, datetime]] = None):
        if date is None:
            date = datetime.utcnow()
        elif isinstance(date, int):
            date = datetime.utcfromtimestamp(date)

        if isinstance(date, datetime):
            date = date.strftime("%d-%m-%Y")

        else:  # it is a str
            try:
                datetime.strptime(date, "%d-%m-%Y")
            except ValueError:  # pragma: no cover
                raise ValueError(
                    "Expected DD-MM-YYYY date format got {!r} ".format(date)
                )

        self.date: str = date  # noqa

    def __hash__(self):  # pragma: no cover
        return hash(self.date)


class Parameters:
    """
    Class to make an obj that will be used as a defaults param in
        getters.

    Parameters
    ----------
        method: :class:`methods.Method` or :class:`int`
            A prayer time calculation method, you can look into all
            methods from :meth:`Client.get_all_methods()`.

            Default: ISNA (Islamic Society of North America).

        tune: Optional[:class:`Tune`]
            To offset returned timings.
            Default: Tune()

        school: :class:`int`
            0 for Shafi (standard), 1 for Hanafi.
            Default: Shafi

        midnightMode: :class:`int`
            0 for Standard (Mid Sunset to Sunrise), 1 for Jafari
            (Mid Sunset to Fajr).
            Default: Standard

        timezonestring: Optional[:class:`str`]
            A valid timezone name as specified on
            https://www.php.net/manual/en/timezones.php

            Example: Europe/London.

            Calculated using the co-ordinates provided by default.

            *This should be used only in getters that uses co-ordinates
            or it will be ignored.*

            *New in v0.2.*

        latitudeAdjustmentMethod: :class:`int`
            Method for adjusting times higher latitudes.
            For instance, if you are checking timings in the UK or Sweden.

            1 - Middle of the Night
            2 - One Seventh
            3 - Angle Based
            Default: Angle Based

        adjustment: :class:`int`
            Number of days to adjust hijri date(s)
            Default: 0

    Attributes
    ----------
        method: :class:`int`
            Method id.

        method_params: Optional[dict[str, int or "null"]]
            Method's parameters. ``None`` if method wasn't custom.

            *New in v0.2.*

        tune: :class:`str`
            Tune Value.

        school: :class:`int`

        midnightMode: :class:`int`

        timezonestring: :class:`str`
            *New in v0.2.*

        latitudeAdjustmentMethod: :class:`int`

        adjustment: :class:`int`

    Raises
    ------
        :exc:`~aladhan.exceptions.InvalidMethod`
            Method id passed was not in 0-15,
            Or passed an integer (99) instead of Method obj for a custom
            method use.

        :exc:`~aladhan.exceptions.InvalidTune`
            Tune with a bad value was passed.

        :exc:`~aladhan.exceptions.InvalidSchool`

        :exc:`~aladhan.exceptions.InvalidMidnightMode`

        :exc:`~aladhan.exceptions.InvalidTimezone`

        :exc:`~aladhan.exceptions.InvalidLatAdjMethod`

        :exc:`~aladhan.exceptions.InvalidAdjustment`
    """

    __slots__ = (
        "method",
        "method_params",
        "tune",
        "school",
        "midnightMode",
        "timezonestring",
        "latitudeAdjustmentMethod",
        "adjustment",
    )

    def __init__(
        self,
        method: Union[Method, int] = ISNA,
        tune: Optional[Tune] = None,
        school: Union[int, Schools] = Schools.SHAFI,
        midnightMode: Union[  # noqa
            int, MidnightModes
        ] = MidnightModes.STANDARD,
        timezonestring: Optional[str] = None,
        latitudeAdjustmentMethod: Union[  # noqa
            int, LatitudeAdjustmentMethods
        ] = LatitudeAdjustmentMethods.ANGLE_BASED,
        adjustment: int = 0,
    ):
        # method
        self.method_params = None
        if isinstance(method, Method):
            if method.id == 99:
                self.method_params = method.params_str
            method = method.id
        elif method == 99:
            raise InvalidMethod(
                "Pass Method object instead if you want to use custom method."
                " for more info https://aladhanpy.readthedocs.io/en/latest/"
                "api.html#aladhan.methods.Method"
            )

        if method not in range(16) and method != 99:  # pragma: no cover
            raise InvalidMethod(
                "Expected method in 0-15 range or 99 got {!r}".format(method)
            )
        self.method: int = method

        # tune
        if tune is None:
            tune = Tune().value
        elif isinstance(tune, Tune):
            tune = tune.value
            ts = tune.split(",")
            if len(ts) != 9 or not all(x.isdigit() for x in ts):
                raise InvalidTune(
                    "Invalid tune argument was passed. (tune.value = %s)"
                    % tune
                )
        else:
            raise InvalidTune(
                "'tune' argument must be `Tune` object."
                " got `%s` instead." % type(tune).__name__
            )
        self.tune: str = tune

        # school
        if isinstance(school, Schools):
            school = school.value
        if school not in (0, 1):  # pragma: no cover
            raise InvalidSchool(
                "School argument can only be either 0 or 1 got {!r}".format(
                    school
                )
            )
        self.school = school

        # midnight mode
        if isinstance(midnightMode, MidnightModes):
            midnightMode = midnightMode.value
        if midnightMode not in (0, 1):  # pragma: no cover
            raise InvalidMidnightMode(
                "midnightMode argument can only be either 0 or 1"
                " got {!r}".format(midnightMode)
            )
        self.midnightMode = midnightMode

        # timezone string
        if timezonestring and timezonestring not in pytz.all_timezones_set:
            raise InvalidTimezone(
                "Invalid timezone ({!r}).".format(timezonestring)
                + " https://www.php.net/manual/en/timezones.php "
                "for valid timezones."
            )

        self.timezonestring: str = timezonestring

        # lat adj methods
        if isinstance(latitudeAdjustmentMethod, LatitudeAdjustmentMethods):
            latitudeAdjustmentMethod = latitudeAdjustmentMethod.value
        if latitudeAdjustmentMethod not in (1, 2, 3):  # pragma: no cover
            raise InvalidLatAdjMethod(
                "latitudeAdjustmentMethod argument can only be either 1, 2 or 3"
                " got {!r}".format(latitudeAdjustmentMethod)
            )
        self.latitudeAdjustmentMethod = latitudeAdjustmentMethod

        # adj
        if not isinstance(adjustment, int):
            raise InvalidAdjustment(
                "Expected adjustment argument to be `int` got"
                " `{}`".format(type(adjustment).__name__)
            )
        self.adjustment = adjustment

    @property
    def as_dict(self):
        dct = {
            "method": self.method,
            "tune": self.tune,
            "school": self.school,
            "midnightMode": self.midnightMode,
            "latitudeAdjustmentMethod": self.latitudeAdjustmentMethod,
            "adjustment": self.adjustment,
        }
        if self.method == 99:
            dct["methodSettings"] = self.method_params
        if self.timezonestring:
            dct["timezonestring"] = self.timezonestring
        return dct

    def __hash__(self):  # pragma: no cover
        return hash(tuple(self.as_dict.values()))


class Meta:
    """Represents the meta that is in returned :class:`Data`

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        data: :class:`Data`
            Original fetched Data.

        longitude: :class:`float`
            Longitude coordinate.

        latitude: :class:`float`
            Latitude coordinate.

        timezone:  :class:`pytz.UTC`
            Used timezone to calculate.

        method: Optional[:class:`Method`]
            Calculation Method. ``None`` if it was a custom method.

        latitudeAdjustmentMethod: :class:`str`

        midnightMode: :class:`str`

        school: :class:`str`

        offset: :class:`Tune`
            Used offset to tune timings.
    """

    __slots__ = (
        "data",
        "longitude",
        "latitude",
        "timezone",
        "method",
        "latitudeAdjustmentMethod",
        "midnightMode",
        "school",
        "offset",
    )

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
        self.method = all_methods.get(method.get("id"))
        self.latitudeAdjustmentMethod = latitudeAdjustmentMethod
        self.midnightMode = midnightMode
        self.school = school
        self.offset = Tune(**offset)

    @property
    def parameters(self):
        """:class:`Parameters`: returns a Parameters obj

        .. warning::
            This will set method to ISNA if method was custom,
             and it will always set adjustment to 0.
        """
        return Parameters(  # TODO: testing
            self.method or 2,
            self.offset,
            getattr(Schools, self.school.upper()),
            getattr(MidnightModes, self.midnightMode.upper()),
            self.timezone.zone,
            getattr(
                LatitudeAdjustmentMethods,
                self.latitudeAdjustmentMethod.upper(),
            )
            # can't get adjustment ...
        )

    def __repr__(self):  # pragma: no cover
        return (
            "<Meta longitude={0.longitude!r}, latitude={0.latitude!r}, "
            "method={0.method!r}, latitudeAdjustmentMethod="
            "{0.latitudeAdjustmentMethod!r}, midnightMode={0.midnightMode!r}, "
            "school={0.school!r}, offset={0.offset!r}>"
        ).format(self)

    def __hash__(self):  # pragma: no cover
        return hash(
            (
                self.method,
                self.longitude,
                self.latitude,
                self.timezone,
                self.method,
                self.latitudeAdjustmentMethod,
                self.method,
                self.school,
                self.offset,
            )
        )


class DateType:
    """A class for gregorian/hijri date.

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        name: :class:`str`
            gregorian or hijri.

        date: :class:`str`
            Date string.

        format: :class:`str`
            Date's format

        day: :class:`int`
            Date's day.

        weekday: dict[:class:`str`, :class:`str`]
            A dict with 2 keys, "en" and "ar" for hijri
            and only 1 key "en" for gregorian.

        month: dict[:class:`str`, :class:`int` or :class:`str`]
            A dict with 3 keys "number", "en", "ar" for hijri
            and 2 keys "number", "en" for gregorian.

        year: :class:`int`
            Date's year.

        designation: dict[:class:`str`, :class:`str`]
            A dict with 2 keys, "abbreviated" and "expanded".

        holidays: Optional[:class:`list` of :class:`str`]
            A list of holidays might be empty for hijri,
            always None for gregorian.
    """

    __slots__ = (
        "name",
        "date",
        "format",
        "day",
        "weekday",
        "month",
        "year",
        "designation",
        "holidays",
    )

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

    def __repr__(self):  # pragma: no cover
        return (
            "<DateType name={0.name!r}, date={0.date!r}, "
            "holidays={0.holidays}>"
        ).format(self)

    def __hash__(self):  # pragma: no cover
        return hash((self.name, self.date))


class Date:
    """Represents the date that is in returned :class:`Data`

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        data: Optional[:class:`Data`]
            Original fetched Data. None if it wasn't from a timings getter.

            *Changed in v1.1.0: changed to Optional*

        readable: Optional[:class:`str`]
            Date in readable format. None if it wasn't from a timings getter.

            *Changed in v1.1.0: changed to Optional*

        timestamp: Optional[:class:`int`]
            Date in UNIX format. None if it wasn't from a timings getter.

            *Changed in v1.1.0: changed to Optional*

        gregorian: :class:`DateType`
            Gregorian date.

        hijri: :class:`DateType`
            Hijri date.
    """

    __slots__ = ("data", "readable", "timestamp", "gregorian", "hijri")

    def __init__(
        self,
        gregorian: dict,
        hijri: dict,
        data: Optional["Data"] = None,
        readable: Optional[str] = None,
        timestamp: Optional[str] = None,
    ):
        self.data = data
        self.readable = readable
        self.timestamp = timestamp and int(timestamp)
        self.gregorian = DateType("Gregorian", **gregorian)
        self.hijri = DateType("Hijri", **hijri)

    def __repr__(self):  # pragma: no cover
        return "gregorian={0.gregorian!r}, hijri={0.hijri!r}>".format(self)

    def __hash__(self):  # pragma: no cover
        return hash(self.timestamp)


class Timings:
    """Represents the timings that is in returned :class:`Data`

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        data: :class:`Data`
            Original fetched Data.

        imsak: :class:`Prayer`
            Imsak time.

        fajr: :class:`Prayer`
            Fajr prayer time.

        sunrise: :class:`Prayer`
            Sunrise time.

        asr: :class:`Prayer`
            Asr prayer time.

        maghrib: :class:`Prayer`
            Maghrib prayer time.

        sunset: :class:`Prayer`
            Sunset time.

        isha: :class:`Prayer`
            Isha prayer time.

        midnight: :class:`Prayer`
            Midnight time.

    *New in v0.1.4: __iter__*
    """

    __slots__ = (
        "data",
        "imsak",
        "fajr",
        "sunrise",
        "dhuhr",
        "asr",
        "maghrib",
        "sunset",
        "isha",
        "midnight",
    )

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
        _Prayer = partial(Prayer, timings=self, date=data.date.gregorian.date)
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
    def as_dict(self) -> Dict[str, Prayer]:
        """dict[:class:`str`, :class:`Prayer`]:
            A dict of all 5 prayers and the other times

        *New in v0.1.4*"""
        return {
            "Imsak": self.imsak,
            "Fajr": self.fajr,
            "Sunrise": self.sunrise,
            "Dhuhr": self.dhuhr,
            "Asr": self.asr,
            "Sunset": self.sunset,
            "Maghrib": self.maghrib,
            "Isha": self.isha,
            "Midnight": self.midnight,
        }

    @property
    def prayers_only(self) -> Dict[str, Prayer]:
        """dict[:class:`str`, :class:`Prayer`]:
        A dict of the 5 prayers."""
        return {
            "Fajr": self.fajr,
            "Dhuhr": self.dhuhr,
            "Asr": self.asr,
            "Maghrib": self.maghrib,
            "Isha": self.isha,
        }

    def next_prayer(self) -> Optional[Prayer]:
        """
        Get the next upcoming prayer.
        Returns ``None`` if the upcoming wasn't in the date,
        so this will return ``None`` if it was from an old date.

        Returns
        -------
            Optional[:class:`Prayer`]
                The upcoming prayer.

        *Changed in v1.0.: Returns None instead of recursive calls,
        and no longer awaitable.*
        """
        meta = self.data.meta
        now = datetime.utcnow()
        now = now + meta.timezone.utcoffset(now)
        for key, val in self.prayers_only.items():
            if now < val.time:
                return val

        return None

    def __iter__(self) -> Iterable[Prayer]:
        yield from self.as_dict.values()

    def __repr__(self):  # pragma: no cover
        return (
            "<Timings imsak={0.imsak}, fajr={0.fajr}, sunrise={0.sunrise}, "
            "dhuhr={0.dhuhr}, asr={0.asr}, sunset={0.sunset}, "
            "maghrib={0.maghrib}, isha={0.isha}, midnight={0.midnight}>"
        ).format(self)

    def __hash__(self):  # pragma: no cover
        return hash(tuple(self.as_dict.values()))


class Data:
    """Main class Representing the data returned from a request to APi

    Do not create this class yourself. Only get it through a getter.

    Attributes
    ----------
        meta: :class:`Meta`
            Represents the meta part.

        date: :class:`Date`
            Represents the date part.

        timings: :class:`Timings`
            Represents the timings part.

        client: :class:`Client`
            Represents the client that the Data were fetched from.
    """

    __slots__ = ("meta", "date", "timings", "client")

    def __init__(self, timings: dict, date: dict, meta: dict, client):
        self.meta = Meta(**meta, data=self)
        self.date = Date(**date, data=self)
        self.timings = Timings(**timings, data=self)
        self.client = client

    def __repr__(self):  # pragma: no cover
        return "<Data object | {0.gregorian.date}>".format(self.date)

    def __hash__(self):  # pragma: no cover
        return hash((self.meta, self.date))

from typing import Awaitable as Aw
from typing import Dict, List, Optional
from typing import Union as Un

from .data_classes import (
    CalendarDateArg,
    Data,
    Date,
    Ism,
    NextPrayerData,
    Parameters,
    Prayer,
    Qibla,
    Timings,
    TimingsDateArg,
)
from .http import HTTPClient
from .methods import Method, all_methods
from .types import IMR, SDR, StatusR

TimingsR = Un[Timings, Aw[Timings]]
_Calendar = Un[List[Timings], Dict[str, Timings]]
CalendarR = Un[_Calendar, Aw[_Calendar]]
QiblaR = Un[Qibla, Aw[Qibla]]
AsmaR = Un[List[Ism], Aw[List[Ism]]]
DateR = Un[Date, Aw[Date]]
LDateR = Un[List[Date], Aw[List[Date]]]
PrayerR = Un[Prayer, Aw[Prayer]]
IntR = Un[int, Aw[int]]
StrR = Un[str, Aw[str]]
ListR = Un[list, Aw[list]]

__all__ = ("Client",)


class Client:
    """
    Al-adhan API client.

    Set to synchronous usage by default, set is_async to True
    if asynchronous usage wanted.

    Auto handles rate limits by default, set auto_manage_rate to False if
    otherwise is wanted. *New in v1.2.0*

    Example

    .. tab:: Synchronous

        .. code:: py

            import aladhan

            client = aladhan.Client()
            times = client.get_timings_by_address("New York")
            print(times)

    .. tab:: Asynchronous

        .. code:: py

            import aladhan, asyncio

            async def main():
                # --- manual closing session
                client = aladhan.Client(is_async=True)
                times = await client.get_timings_by_address("New York")
                print(times)
                await client.close()

                # --- using context
                async with aladhan.Client(is_async=True) as client:
                    times = await client.get_timings_by_address("New York")
                    print(times)

            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())

    .. note::
        For Asynchronous usage you need to initialize this class in
        a |coroutine_link|_.

    Parameters
    ----------
        is_async: :class:`bool`
            Whether to be used asynchronously or not.

        auto_manage_rate: :class:`bool`
            Whether to handle rate limits automatically or not.
    """

    __slots__ = "converter", "http"

    def __init__(self, is_async: bool = False, auto_manage_rate: bool = True):
        self.converter = is_async and _AsyncConverter or _SyncConverter
        self.http = HTTPClient(
            is_async=is_async, auto_manage_rate=auto_manage_rate
        )

    def close(self):
        """Closes the connection."""
        return self.http.close()  # this can be a coroutine

    @property
    def is_async(self) -> bool:
        return self.http.is_async

    def __enter__(self):
        if self.is_async:  # pragma: no cover
            raise TypeError(
                "Asynchronous client must be used in an asynchronous context"
                "manager (async with) not in a synchronous one (with)."
            )
        return self

    def __exit__(self, *_):
        self.close()

    async def __aenter__(self):
        if not self.is_async:  # pragma: no cover
            raise TypeError(
                "Synchronous client must be used in a synchronous context"
                "manager (with) not in an asynchronous one (async with)."
            )
        return self

    async def __aexit__(self, *_):
        await self.close()

    def get_next_prayer_by_address(
        self,
        address: str,
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ) -> PrayerR:
        """
        Get next upcoming prayer from address.

        Parameters
        ----------
            address: :class:`str`
                An address string.
                Example: "London, United Kingdom"

            date: Optional[:class:`TimingsDateArg`]
                Date for the prayer times.
                Default: Current date.

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`Prayer`
                Prayer obj from the API response.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

        *New in v1.2.0*
        """
        date = date and date.date or ""
        params = (params or Parameters()).as_dict
        params.update(dict(address=address))
        return self.converter.to_prayer(
            self,
            self.http.get_next_prayer_by_address(date, params),
        )

    def get_timings(
        self,
        longitude: Un[int, float],
        latitude: Un[int, float],
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ) -> TimingsR:
        """
        Get prayer times from coordinates (longitude, latitude).

        Parameters
        ----------
            longitude: :class:`int` or :class:`float`
                Longitude coordinate of the location.

            latitude: :class:`int` or :class:`float`
                Latitude coordinate of the location.

            date: Optional[:class:`TimingsDateArg`]
                Date for the prayer times.
                Default: Current date.

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`Timings`
                Timings obj from the API response.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.
        """
        date = date and date.date or ""
        params = (params or Parameters()).as_dict
        params.update(dict(longitude=str(longitude), latitude=str(latitude)))
        return self.converter.to_timings(
            self, self.http.get_timings(date, params)
        )

    def get_timings_by_address(
        self,
        address: str,
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ) -> TimingsR:
        """
        Get prayer times from address.

        Parameters
        ----------
            address: :class:`str`
                An address string.
                Example: "London, United Kingdom"

            date: Optional[:class:`TimingsDateArg`]
                Date for the prayer times.
                Default: Current date.

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`Timings`
                Timings obj from the API response.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.
        """
        date = date and date.date or ""
        params = (params or Parameters()).as_dict
        params.update(dict(address=address))
        return self.converter.to_timings(
            self, self.http.get_timings_by_address(date, params)
        )

    def get_timings_by_city(
        self,
        city: str,
        country: str,
        state: Optional[str] = None,
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ) -> TimingsR:
        """
        Get prayer times from city, country and state.

        Parameters
        ----------
            city: :class:`str`
                The city name.
                Example: "London"

            country: :class:`str`
                The country name or 2 character alpha ISO 3166 code.
                Example: "GB" or "United Kingdom"

            state: Optional[:class:`str`]
                State or province. The state name or abbreviation..
                Example: "Bexley"

            date: Optional[:class:`TimingsDateArg`]
                Date for the prayer times.
                Default: Current date.

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`Timings`
                Timings obj from the API response.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.
        """
        date = date and date.date or ""
        params = (params or Parameters()).as_dict
        params.update(dict(city=city, country=country, state=state))
        if state is None:
            del params["state"]
        return self.converter.to_timings(
            self, self.http.get_timings_by_city(date, params)
        )

    def get_calendar(
        self,
        longitude: Un[int, float],
        latitude: Un[int, float],
        date: CalendarDateArg,
        params: Optional[Parameters] = None,
    ) -> CalendarR:
        """
        Get all prayer times for a specific calendar month/year from \
        coordinates (longitude, latitudes).

        Parameters
        ----------
            longitude: :class:`int` or :class:`float`
                Longitude coordinate of the location.

            latitude: :class:`int` or :class:`float`
                Latitude coordinate of the location.

            date: :class:`CalendarDateArg`
                Date for the prayer times.

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`list` of :class:`Timings` or dict[:class:`str`, \
            :class:`list` of :class:`Timings`]
                A month calendar if month parameter was given in date
                argument otherwise a year calendar.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.
        """
        params = (params or Parameters()).as_dict
        params.update(longitude=str(longitude), latitude=str(latitude))
        params.update(date.as_dict)
        return self.converter.to_timings(
            self, self.http.get_calendar(params, date.hijri)
        )

    def get_calendar_by_address(
        self,
        address: str,
        date: CalendarDateArg,
        params: Optional[Parameters] = None,
    ) -> CalendarR:
        """
        Get all prayer times for a specific calendar month/year
            from address.

        Parameters
        ----------
            address: :class:`str`
                An address string.
                Example: "London, United Kingdom"

            date: :class:`CalendarDateArg`
                Date for the prayer times.

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`list` of :class:`Timings` or dict[:class:`str`, \
            :class:`list` of :class:`Timings`]
                A month calendar if month parameter was given in date
                argument otherwise a year calendar.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.
        """
        params = (params or Parameters()).as_dict
        params.update(dict(address=address))
        params.update(date.as_dict)
        return self.converter.to_timings(
            self,
            self.http.get_calendar_by_address(params, date.hijri),
        )

    def get_calendar_by_city(
        self,
        city: str,
        country: str,
        date: CalendarDateArg,
        state: Optional[str] = None,
        params: Optional[Parameters] = None,
    ) -> CalendarR:
        """
        Get all prayer times for a specific calendar month/year
            from address.

        Parameters
        ----------
            city: :class:`str`
                The city name.
                Example: "London"

            country: :class:`str`
                The country name or 2 character alpha ISO 3166 code.
                Example: "GB" or "United Kingdom"

            date: :class:`CalendarDateArg`
                Date for the prayer times.

            state: Optional[:class:`str`]
                State or province. The state name or abbreviation..
                Example: "Bexley"

            params: Optional[:class:`Parameters`]
                Default: ``Parameters()``

        Returns
        -------
            :class:`list` of :class:`Timings` or dict[:class:`str`, \
            :class:`list` of :class:`Timings`]
                A month calendar if month parameter was given in date
                argument otherwise a year calendar.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.
        """
        params = (params or Parameters()).as_dict
        params.update(dict(city=city, country=country, state=state))
        if state is None:
            del params["state"]
        params.update(date.as_dict)
        return self.converter.to_timings(
            self, self.http.get_calendar_by_city(params, date.hijri)
        )

    @staticmethod
    def get_all_methods() -> Dict[int, Method]:
        """
        Gives all available prayer times calculation method.

        Returns
        -------
            dict[:class:`int`, :class:`Method`]
                A dict of available calculation method from 0 to 15.
        """
        return all_methods

    def get_qibla(
        self, longitude: Un[int, float], latitude: Un[int, float]
    ) -> QiblaR:
        """
        Get the Qibla direction from a pair of coordinates.

        Parameters
        ----------
            longitude: :class:`int` or :class:`float`
                Longitude co-ordinate.

            latitude: :class:`int` or :class:`float`
                Latitude co-ordinate.

        Returns
        -------
            :class:`Qibla`
                The qibla.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

        *New in v0.1.3*
        """
        return self.converter.to_obj_kwa(
            self.http.get_qibla(latitude, longitude), Qibla
        )

    def get_asma(self, *n: int) -> AsmaR:
        """
        Returns a list of asma from giving numbers.

        Parameters
        ----------
            n: :class:`int`
                Numbers from range 1-99.

        Returns
        -------
            :class:`list` of :class:`Ism`
                A list of asma.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

        *New in v0.1.3*
        """

        assert n, "No arguments was passed."
        return self.converter.to_list_of_obj(
            self.http.get_asma(",".join(map(str, n))), Ism
        )

    def get_all_asma(self) -> AsmaR:
        """
        Returns all 1-99 asma (allah names).

        Returns
        -------
            :class:`list` of :class:`Ism`
                A list of all asma.

        *New in v0.1.3*
        """
        return self.get_asma(*range(1, 100))

    def get_hijri_from_gregorian(
        self, date: Optional[TimingsDateArg] = None, adjustment: int = 0
    ) -> DateR:
        """
        Convert a gregorian date to a hijri date.

        Parameters
        ----------
            date: Optional[:class:`TimingsDateArg`]
                Gregorian date.
                Default: Current date

            adjustment: Optional[:class:`int`]
                Number of days to adjust.
                Default: 0

        Returns
        -------
            :class:`Date`
                Date in hijri.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid date or unable to convert it.

        *New in v1.1.0*
        """
        return self.converter.to_obj_kwa(
            self.http.get_hijri_from_gregorian(
                date=date.date, adjustment=adjustment
            ),
            Date,
        )

    def get_gregorian_from_hijri(
        self, date: TimingsDateArg, adjustment: int = 0
    ) -> DateR:
        """
        Convert a hijri date to a gregorian date.

        Parameters
        ----------
            date: Optional[:class:`TimingsDateArg`]
                Gregorian date.
                Default: Current date

            adjustment: Optional[:class:`int`]
                Number of days to adjust.
                Default: 0

        Returns
        -------
            :class:`Date`
                Date in gregorian.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid date or unable to convert it.

        *New in v1.1.0*
        """
        return self.converter.to_obj_kwa(
            self.http.get_gregorian_from_hijri(
                date=date.date, adjustment=adjustment
            ),
            Date,
        )

    def get_hijri_calendar_from_gregorian(
        self, month: int, year: int, adjustment: int = 0
    ) -> LDateR:
        """
        Get a hijri calendar for a gregorian month.

        Parameters
        ----------
            month: :class:`int`
                Gregorian month.

            year: :class:`int`
                Gregorian year.

            adjustment: Optional[:class:`int`]
                Number of days to adjust.
                Default: 0

        Returns
        -------
            :class:`list` of :class:`Date`
                Hijri Calendar.

        *New in v1.1.0*
        """
        return self.converter.to_list_of_obj(
            self.http.get_hijri_calendar_from_gregorian(
                month, year, adjustment
            ),
            Date,
        )

    def get_gregorian_calendar_from_hijri(
        self, month: int, year: int, adjustment: int = 0
    ) -> LDateR:
        """
        Get a gregorian calendar for a hijri month.

        Parameters
        ----------
            month: :class:`int`
                Hijri month.

            year: :class:`int`
                Hijri year.

            adjustment: Optional[:class:`int`]
                Number of days to adjust.
                Default: 0

        Returns
        -------
            :class:`list` of :class:`Date`
                Gregorian Calendar.

        *New in v1.1.0*
        """
        return self.converter.to_list_of_obj(
            self.http.get_gregorian_calendar_from_hijri(
                month, year, adjustment
            ),
            Date,
        )

    def get_islamic_year_from_gregorian_for_ramadan(self, year: int) -> int:
        """
        Get which islamic year for ramadan from a gregorian year.

        Parameters
        ----------
            year: :class:`int`
                Gregorian year.

        Returns
        -------
            :class:`int`
                Hijri year.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Unable to compute year.
        """
        return self.converter.to_obj_a(
            self.http.get_islamic_year_from_gregorian_for_ramadan(year), int
        )

    def get_current_time(self, zone: str) -> StrR:
        """
        Parameters
        ----------
            zone: :class:`str`
                Timezone string. ex: `"Europe/London"`

        Returns
        -------
            :class:`str`
                The current time for the specified time zone.
                ex: `"13:56"`

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid timezone.
        """
        return self.http.get_current_time(zone=zone)

    def get_current_date(self, zone: str) -> StrR:
        """
        Parameters
        ----------
            zone: :class:`str`
                Timezone string. ex: `"Europe/London"`

        Returns
        -------
            :class:`str`
                The current Date for the specified time zone in DD-MM-YYYY.
                ex: `"23-02-2021"`

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid timezone.
        """
        return self.http.get_current_date(zone=zone)

    def get_current_timestamp(self, zone: str) -> IntR:
        """
        Parameters
        ----------
            zone: :class:`str`
                Timezone string. ex: `"Europe/London"`

        Returns
        -------
            :class:`int`
                The current UNIX timestamp for the specified time zone.
                ex: `1503495668`

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid timezone.
        """
        return self.converter.to_obj_a(
            self.http.get_current_timestamp(zone=zone), int
        )

    def get_current_islamic_year(self, adjustment: int = 0) -> IntR:
        """
        Parameters
        ----------
            adjustment: :class:`int`
                Number of days to adjust hijri date.

        Returns
        -------
            :class:`int`
                The current islamic year.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Unable to compute year.
        """
        return self.converter.to_obj_a(
            self.http.get_current_islamic_year(adjustment=adjustment), int
        )

    def get_current_islamic_month(self, adjustment: int = 0) -> IntR:
        """
        Parameters
        ----------
            adjustment: :class:`int`
                Number of days to adjust hijri date.

        Returns
        -------
            :class:`int`
                The current islamic month.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Unable to compute month.
        """
        return self.converter.to_obj_a(
            self.http.get_current_islamic_month(adjustment=adjustment), int
        )

    def get_next_hijri_holiday(self, adjustment: int = 0) -> DateR:
        """
        Parameters
        ----------
            adjustment: :class:`int`
                Number of days to adjust hijri date.

        Returns
        -------
            :class:`~aladhan.Date`
                The Next upcoming hijri holiday.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Unable to compute next holiday.
        """
        return self.converter.to_obj_kwa(
            self.http.get_next_hijri_holiday(adjustment=adjustment), Date
        )

    def get_hijri_holidays(self, day: int, month: int) -> ListR:
        """
        Parameters
        ----------
            day: :class:`int`
                Hijri day.
            month: :class:`int`
                Hijri month.

        Returns
        -------
            :class:`list` of :class:`str`
                All day's holidays, can be empty list.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Invalid day or month.
        """
        return self.http.get_hijri_holidays(day, month)

    def get_islamic_holidays(self, year: int, adjustment: int = 0) -> LDateR:
        """
        Parameters
        ----------
            year: :class:`int`
                Hijri year.
            adjustment: :class:`int`
                Number of days to adjust hijri date.

        Returns
        -------
            :class:`list` of :class:`~aladhan.Date`
                All year's holidays, 19 in total.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Something went wrong.
        """
        return self.converter.to_list_of_obj(
            self.http.get_hijri_holidays(year, adjustment), Date
        )

    def get_status(self) -> StatusR:
        """
        Returns
        -------
            :class:`dict`
                Api's status.

        Raises
        ------
            :exc:`~aladhan.exceptions.InternalServerError`
               Status Check Failed.
        """
        return self.http.get_status()

    def get_special_days(self) -> SDR:
        """
        Get all islamic special days (holidays).

        Returns
        -------
            :class:`list` of :class:`dict`
                A list of all special days with ``day,month,name`` keys.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Something went wrong.
        """
        return self.http.get_special_days()

    def get_islamic_months(self) -> IMR:
        """
        Get all 12 islamic months.

        Returns
        -------
            :class:`dict` of :class:`str` and :class:`dict`
                A dict of '1' to '12' as keys and dicts of ``number,en,ar`` keys.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
               Something went wrong.
        """
        return self.http.get_islamic_months()


def _decide_timings(client, data):

    if isinstance(data, list):  # it is a month calendar
        return [Data(**day, client=client).timings for day in data]
    # it is a dict
    if "1" in data:  # it is a year calendar
        return {
            month: [Data(**day, client=client).timings for day in days]
            for month, days in data.items()
        }

    # it is just a day timings
    return Data(**data, client=client).timings


class _SyncConverter:
    @staticmethod
    def to_prayer(client, o):
        return NextPrayerData(client=client, **o).prayer

    @staticmethod
    def to_timings(client, o):
        return _decide_timings(client, o)

    @staticmethod
    def to_obj_a(o, obj):
        return obj(o)

    @staticmethod
    def to_obj_kwa(o, obj):
        return obj(**o)

    @staticmethod
    def to_list_of_obj(o, obj):
        return [obj(**d) for d in o]


class _AsyncConverter:
    @staticmethod
    async def to_prayer(client, o):
        return NextPrayerData(client=client, **(await o)).prayer

    @staticmethod
    async def to_timings(client, o):
        return _decide_timings(client, await o)

    @staticmethod
    async def to_obj_a(o, obj):
        return obj(await o)

    @staticmethod
    async def to_obj_kwa(o, obj):
        return obj(**(await o))

    @staticmethod
    async def to_list_of_obj(o, obj):
        return [obj(**d) for d in await o]

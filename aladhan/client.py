from .methods import all_methods, Method
from .base_types import (
    Timings,
    Data,
    TimingsDateArg,
    Parameters,
    CalendarDateArg,
    Qibla,
    Ism,
    Date,
)
from .http import HTTPClient

from typing import (
    Awaitable as A,
    Union as U,
    Optional,
    List,
    Dict,
)

TimingsR = U[Timings, A[Timings]]
_Calendar = U[List[Timings], Dict[str, Timings]]
CalendarR = U[_Calendar, A[_Calendar]]
QiblaR = U[Qibla, A[Qibla]]
AsmaR = U[List[Ism], A[List[Ism]]]
DateR = U[Date, A[Date]]
LDateR = U[List[Date], A[List[Date]]]
IntR = U[int, A[int]]
StrR = U[str, A[str]]

__all__ = ("Client",)


class Client:
    """
    Al-adhan API client.

    Set to synchronous usage by default, set is_async to True
        if asynchronous usage wanted.

    Synchronous example

    .. code:: py

        import aladhan

        client = aladhan.Client()
        times = client.get_timings_by_address("New York")
        print(times)

    Asynchronous example

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
        For Asynchronous usage you need to initialize
            this class in a |coroutine_link|_.
    """

    __slots__ = "converter", "http"

    def __init__(self, is_async: bool = False):
        self.converter = is_async and _AsyncConverter or _SyncConverter
        self.http = HTTPClient(is_async=is_async)

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

    def get_timings(
        self,
        longitude: U[int, float],
        latitude: U[int, float],
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ) -> TimingsR:
        """
        Get prayer times from coordinates (longitude, latitude).

        Parameters
        -----------
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
        date = (date or TimingsDateArg()).date
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
        -----------
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
        date = (date or TimingsDateArg()).date
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
        -----------
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
        date = (date or TimingsDateArg()).date
        params = (params or Parameters()).as_dict
        params.update(dict(city=city, country=country, state=state))
        if state is None:
            del params["state"]
        return self.converter.to_timings(
            self, self.http.get_timings_by_city(date, params)
        )

    def get_calendar(
        self,
        longitude: U[int, float],
        latitude: U[int, float],
        date: CalendarDateArg,
        params: Optional[Parameters] = None,
    ) -> CalendarR:
        """
        Get all prayer times for a specific calendar month/year from \
        coordinates (longitude, latitudes).

        Parameters
        -----------
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
        -----------
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
        self, longitude: U[int, float], latitude: U[int, float]
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


class _SyncConverter:
    @staticmethod
    def to_timings(client, o):

        data = o
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
    async def to_timings(client, o):

        data = await o
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

    @staticmethod
    async def to_obj_a(o, obj):
        return obj(await o)

    @staticmethod
    async def to_obj_kwa(o, obj):
        return obj(**(await o))

    @staticmethod
    async def to_list_of_obj(o, obj):
        return [obj(**d) for d in await o]

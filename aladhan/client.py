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
    Awaitable,
    Optional,
    Union,
    List,
    Dict,
)

TimingsR = Union[Timings, Awaitable[Timings]]
_Calendar = Union[List[Timings], Dict[str, Timings]]
CalendarR = Union[_Calendar, Awaitable[_Calendar]]
QiblaR = Union[Qibla, Awaitable[Qibla]]
AsmaR = Union[List[Ism], Awaitable[List[Ism]]]
DateR = Union[Date, Awaitable[Date]]
LDateR = Union[List[Date], Awaitable[List[Date]]]

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
        longitude: Union[int, float],
        latitude: Union[int, float],
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
        longitude: Union[int, float],
        latitude: Union[int, float],
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
        self, longitude: Union[int, float], latitude: Union[int, float]
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
        return self.converter.to_qibla(
            self.http.get_qibla((latitude, longitude))
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
        return self.converter.to_asma(
            self.http.get_asma(",".join(map(str, n)))
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
        params = dict(date=date.date, adjustment=adjustment)
        return self.converter.to_date(
            self.http.get_hijri_from_gregorian(params)
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
        params = dict(date=date.date, adjustment=adjustment)
        return self.converter.to_date(
            self.http.get_gregorian_from_hijri(params)
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
        return self.converter.to_calendar(
            self.http.get_hijri_calendar_from_gregorian(
                (month, year, adjustment)
            )
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
        return self.converter.to_calendar(
            self.http.get_gregorian_calendar_from_hijri(
                (month, year, adjustment)
            )
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
        return self.converter.to_int(
            self.http.get_islamic_year_from_gregorian_for_ramadan(year)
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
    def to_qibla(o):
        return Qibla(**o)

    @staticmethod
    def to_asma(o):
        return [Ism(**d) for d in o]

    @staticmethod
    def to_date(o):
        return Date(**o)

    @staticmethod
    def to_calendar(o):
        return [Date(**d) for d in o]

    @staticmethod
    def to_int(o):
        return int(o)


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
    async def to_qibla(o):
        return Qibla(**(await o))

    @staticmethod
    async def to_asma(o):
        return [Ism(**d) for d in await o]

    @staticmethod
    async def to_date(o):
        return Date(**(await o))

    @staticmethod
    async def to_calendar(o):
        return [Date(**d) for d in await o]

    @staticmethod
    async def to_int(o):
        return int(await o)

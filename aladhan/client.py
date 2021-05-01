import asyncio
import aiohttp
import platform

from beartype import beartype
from typing import Union, Dict, List, Tuple, Any

from .methods import all_methods
from .base_types import *
from .endpoints import EndPoints

from functools import wraps


#  https://github.com/aio-libs/aiohttp/issues/4324#issuecomment-733884349
if platform.system() == 'Windows':
    from asyncio.proactor_events import _ProactorBasePipeTransport  # noqa

    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise

        return wrapper

    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


class AsyncClient:
    """Asynchronous al-adhan API client.

    .. note::
        You need to initialize this class in a |coroutine_link|_.
        When you finish using the Client, you need to close the session with :meth:`close`.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self._loop = loop or asyncio.get_event_loop()

    async def __get_res(
        self,
        endpoint: str,
        params: Tuple[
            Union[str, Any], ...
        ],  # using tuple cause dict isn't hashable to cache
    ) -> Union[Timings, List[Timings], Dict[str, List[Timings]]]:
        async with aiohttp.ClientSession(loop=self._loop) as session:
            res = await session.get(endpoint, params=dict(params))
            res = await res.json()
        data = res["data"]

        if isinstance(data, str):  # something wrong
            raise Exception(data)
        elif isinstance(data, list):  # it is a month calendar
            return [Data(**day, client=self).timings for day in data]
        # it is a dict

        if "1" in data:  # it is a year calendar
            return {
                month: [Data(**day, client=self).timings for day in days]
                for month, days in data.items()
            }
        return Data(**data, client=self).timings  # it is just a day timings

    @beartype
    async def get_timings(
        self,
        longitude: Union[int, float],
        latitude: Union[int, float],
        date: TimingsDateArg = None,
        defaults: DefaultArgs = None,
    ):
        """|coro|

        Get prayer times from coordinates (longitude, latitude).

        Parameters
        -----------
            longitude: :class:`int` or :class:`float`
                Longitude coordinate of the location.

            latitude: :class:`int` or :class:`float`
                Latitude coordinate of the location.

            date: :class:`TimingsDateArg`
                Date for the prayer times.
                Default: Current date.

            defaults: :class:`DefaultArgs`
                Default params.
                Default: ``DefaultArgs()``

        Returns
        -------
            :class:`Timings`
                Timings obj from the API response.
        """
        params = {
            "longitude": str(longitude),
            "latitude": str(latitude),
        }
        date, defaults = date or TimingsDateArg(), defaults or DefaultArgs()
        params.update(defaults.as_dict)
        return await self.__get_res(
            EndPoints.TIMINGS + "/" + date.date, tuple(params.items())
        )

    @beartype
    async def get_timings_by_address(
        self,
        address: str,
        date: TimingsDateArg = None,
        defaults: DefaultArgs = None,
    ):
        """|coro|
        Get prayer times from address.

        Parameters
        -----------
            address: :class:`str`
                An address string.
                Example: "London, United Kingdom"

            date: :class:`TimingsDateArg`
                Date for the prayer times.
                Default: Current date.

            defaults: :class:`DefaultArgs`
                Default params.
                Default: ``DefaultArgs()``

        Returns
        -------
            :class:`Timings`
                Timings obj from the API response.
        """
        params = {
            "address": address,
        }
        date, defaults = date or TimingsDateArg(), defaults or DefaultArgs()
        params.update(defaults.as_dict)
        return await self.__get_res(
            EndPoints.TIMINGS_BY_ADDRESS + "/" + date.date,
            tuple(params.items()),
        )

    @beartype
    async def get_timings_by_city(
        self,
        city: str,
        country: str,
        state: str = None,
        date: TimingsDateArg = None,
        defaults: DefaultArgs = None,
    ):
        """|coro|
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

            date: :class:`TimingsDateArg`
                Date for the prayer times.
                Default: Current date.

            defaults: :class:`DefaultArgs`
                Default params.
                Default: ``DefaultArgs()``

        Returns
        -------
            :class:`Timings`
                Timings obj from the API response.
        """
        params = {
            "city": city,
            "country": country,
            "state": state,
        }
        if state is None:
            del params["state"]
        date, defaults = date or TimingsDateArg(), defaults or DefaultArgs()
        params.update(defaults.as_dict)
        return await self.__get_res(
            EndPoints.TIMINGS_BY_CITY + "/" + date.date, tuple(params.items())
        )

    @beartype
    async def get_calendar(
        self,
        longitude: Union[int, float],
        latitude: Union[int, float],
        date: CalendarDateArg,
        defaults: DefaultArgs = None,
    ):
        """|coro|

        Get all prayer times for a specific calendar month/year from coordinates (longitude, latitudes).

        Parameters
        -----------
            longitude: :class:`int` or :class:`float`
                Longitude coordinate of the location.

            latitude: :class:`int` or :class:`float`
                Latitude coordinate of the location.

            date: :class:`CalendarDateArg`
                Date for the prayer times.

            defaults: :class:`DefaultArgs`
                Default params.
                Default: ``DefaultArgs()``

        Returns
        -------
            :class:`list` of :class:`Timings` or dict[:class:`str`, :class:`list` of :class:`Timings`]
                A month calendar if month parameter was given in date argument otherwise a year calendar.
        """
        params = {
            "longitude": str(longitude),
            "latitude": str(latitude),
        }
        defaults = defaults or DefaultArgs()
        params.update(defaults.as_dict)
        params.update(date.as_dict)
        return await self.__get_res(
            getattr(EndPoints, "HIJRI_" * date.hijri + "CALENDAR"),
            tuple(params.items()),
        )

    @beartype
    async def get_calendar_by_address(
        self, address: str, date: CalendarDateArg, defaults: DefaultArgs = None
    ):
        """|coro|

        Get all prayer times for a specific calendar month/year from address.

        Parameters
        -----------
            address: :class:`str`
                An address string.
                Example: "London, United Kingdom"

            date: :class:`CalendarDateArg`
                Date for the prayer times.

            defaults: :class:`DefaultArgs`
                Default params.
                Default: ``DefaultArgs()``

        Returns
        -------
            :class:`list` of :class:`Timings` or dict[:class:`str`, :class:`list` of :class:`Timings`]
                A month calendar if month parameter was given in date argument otherwise a year calendar.
        """
        params = {"address": address}
        defaults = defaults or DefaultArgs()
        params.update(defaults.as_dict)
        params.update(date.as_dict)
        return await self.__get_res(
            getattr(EndPoints, "HIJRI_" * date.hijri + "CALENDAR_BY_ADDRESS"),
            tuple(params.items()),
        )

    @beartype
    async def get_calendar_by_city(
        self,
        city: str,
        country: str,
        date: CalendarDateArg,
        state: str = None,
        defaults: DefaultArgs = None,
    ):
        """|coro|

        Get all prayer times for a specific calendar month/year from address.

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

            date: :class:`CalendarDateArg`
                Date for the prayer times.

            defaults: :class:`DefaultArgs`
                Default params.
                Default: ``DefaultArgs()``

        Returns
        -------
            :class:`list` of :class:`Timings` or dict[:class:`str`, :class:`list` of :class:`Timings`]
                A month calendar if month parameter was given in date argument otherwise a year calendar.
        """
        params = {
            "city": city,
            "country": country,
            "state": state,
        }
        if state is None:
            del params["state"]
        defaults = defaults or DefaultArgs()
        params.update(defaults.as_dict)
        params.update(date.as_dict)
        return await self.__get_res(
            getattr(EndPoints, "HIJRI_" * date.hijri + "CALENDAR_BY_CITY"),
            tuple(params.items()),
        )

    @staticmethod
    def get_all_methods():
        """
        Gives all available prayer times calculation method.

        Returns
        -------
            :class:`dict`[:class:`int`, :class:`Method`]
                A dict of available calculation method from 0 to 15.
        """
        return all_methods

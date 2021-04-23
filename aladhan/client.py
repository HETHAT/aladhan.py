import asyncio
import aiohttp

from async_lru import alru_cache
from beartype import beartype
from typing import Union, Dict, List, Tuple, Any

from .methods import all_methods
from .base_types import *
from .endpoints import EndPoints


class AsyncClient:
    """Asynchronous al-adhan API client."""

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        """
        :param loop: the event loop for ClientSession, default to
        asyncio.get_event_loop()
        """
        self.loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=self.loop)

    @alru_cache()
    async def __get_res(
        self,
        endpoint: str,
        params: Tuple[
            Union[str, Any], ...
        ],  # using tuple cause dict isn't hashable to cache
    ) -> Union[Data, List[Data], Dict[str, List[Data]]]:
        """. - ."""
        res = await self._session.get(endpoint, params=dict(params))
        res = await res.json()

        data = res["data"]

        if isinstance(data, str):  # something wrong
            raise Exception(data)
        elif isinstance(data, list):  # it is a month calendar
            return [Data(**day, client=self) for day in data]
        # it is a dict

        if "1" in data:  # it is a year calendar
            return {
                month: [Data(**day, client=self) for day in days] for month, days in data.items()
            }
        return Data(**data, client=self)  # it is just a day timings

    @beartype
    async def get_timings(
        self,
        longitude: Union[int, float],
        latitude: Union[int, float],
        date: TimingsDateArg = None,
        defaults: DefaultArgs = None,
    ):
        """
        get prayer times from coordinates (longitude, latitude).

        :param longitude: longitude coordinate of the location
        :param latitude: latitude coordinate of the location
        :param date: date for the prayer times
        :param defaults: default params
        :return: Data object
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
        """
        get prayer times from address.

        :param address: an address string.
        Example: Sultanahmet Mosque, Istanbul, Turkey
        :param date: date for the prayer times
        :param defaults: default params
        :return: Data object
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
        """
        get prayer times from city, country and state.

        :param city: A city name. Example: London
        :param country: A country name or 2 character alpha ISO 3166 code. Examples: GB or United Kingdom
        :param state: (Optional) State or province. A state name or abbreviation.
        Examples: Colorado / CO / Punjab / Bengal
        :param date: date for the prayer times
        :param defaults: default params
        :return: Data object
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
        """
        get all prayer times for a specific calendar month/year from coordinates (longitude, latitudes).

        :param longitude: longitude coordinate of the location
        :param latitude: latitude coordinate of the location
        :param date: date for the prayer times
        :param defaults: default params
        :return: a list of Data object if it was a month calendar and
        a dict of months and list of Data object if it was a year calendar
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
        """
        get all prayer times for a specific calendar month/year from address.

        :param address: an address string.
        Example: Sultanahmet Mosque, Istanbul, Turkey
        :param date: date for the prayer times
        :param defaults: default params
        :return: a list of Data object if it was a month calendar and
        a dict of months and list of Data object if it was a year calendar
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
        """
        get all prayer times for a specific calendar month/year from city, country and state.

        :param city: A city name. Example: London
        :param country: A country name or 2 character alpha ISO 3166 code. Examples: GB or United Kingdom
        :param state: (Optional) State or province. A state name or abbreviation.
        Examples: Colorado / CO / Punjab / Bengal
        :param date: date for the prayer times
        :param defaults: default params
        :return: a list of Data object if it was a month calendar and
        a dict of months and list of Data object if it was a year calendar
        """
        params = {
            "endpoint": "ByCity",
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
        """give all available prayer times calculation method"""
        return all_methods

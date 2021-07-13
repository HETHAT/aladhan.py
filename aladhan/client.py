import aiohttp

from typing import Union, Dict, List, Optional

from .methods import all_methods
from .endpoints import EndPoints
from .exceptions import HTTPException
from .base_types import (
    Timings,
    Data,
    TimingsDateArg,
    Parameters,
    CalendarDateArg,
    Qibla,
    Ism,
)


class AsyncClient:
    """Asynchronous al-adhan API client.

    .. note::
        You need to initialize this class in a |coroutine_link|_.
    """

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.__session = session or aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return exc_type is None

    async def close(self):
        """Closes the connection."""
        await self.__session.close()

    async def _get_res(self, endpoint: str, params: dict) -> dict:
        async with self.__session.get(endpoint, params=params) as res:
            res = await res.json()

        if res["code"] != 200:  # something wrong
            raise HTTPException.from_res(res)
        return res

    async def _get_timings(
        self, endpoint: str, params: dict
    ) -> Union[Timings, List[Timings], Dict[str, List[Timings]]]:

        data = (await self._get_res(endpoint, params))["data"]

        if isinstance(data, list):  # it is a month calendar
            return [Data(**day, client=self).timings for day in data]
        # it is a dict
        if "1" in data:  # it is a year calendar
            return {
                month: [Data(**day, client=self).timings for day in days]
                for month, days in data.items()
            }
        return Data(**data, client=self).timings  # it is just a day timings

    async def get_timings(
        self,
        longitude: Union[int, float],
        latitude: Union[int, float],
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ):
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

            :exc:`~aladhan.exceptions.InternalServerError`
        """
        parameters = {
            "longitude": str(longitude),
            "latitude": str(latitude),
        }
        date, params = date or TimingsDateArg(), params or Parameters()
        parameters.update(params.as_dict)
        return await self._get_timings(
            EndPoints.TIMINGS + "/" + date.date, parameters
        )

    async def get_timings_by_address(
        self,
        address: str,
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ):
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

            :exc:`~aladhan.exceptions.InternalServerError`
        """
        parameters = {
            "address": address,
        }
        date, params = date or TimingsDateArg(), params or Parameters()
        parameters.update(params.as_dict)
        return await self._get_timings(
            EndPoints.TIMINGS_BY_ADDRESS + "/" + date.date, parameters
        )

    async def get_timings_by_city(
        self,
        city: str,
        country: str,
        state: Optional[str] = None,
        date: Optional[TimingsDateArg] = None,
        params: Optional[Parameters] = None,
    ):
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

            :exc:`~aladhan.exceptions.InternalServerError`
        """
        parameters = {
            "city": city,
            "country": country,
            "state": state,
        }
        if state is None:
            del parameters["state"]
        date, params = date or TimingsDateArg(), params or Parameters()
        parameters.update(params.as_dict)
        return await self._get_timings(
            EndPoints.TIMINGS_BY_CITY + "/" + date.date, parameters
        )

    async def get_calendar(
        self,
        longitude: Union[int, float],
        latitude: Union[int, float],
        date: CalendarDateArg,
        params: Optional[Parameters] = None,
    ):
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
                A month calendar if month parameter was given in date argument \
                otherwise a year calendar.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

            :exc:`~aladhan.exceptions.InternalServerError`
        """
        parameters = {
            "longitude": str(longitude),
            "latitude": str(latitude),
        }
        params = params or Parameters()
        parameters.update(params.as_dict)
        parameters.update(date.as_dict)
        return await self._get_timings(
            getattr(EndPoints, "HIJRI_" * date.hijri + "CALENDAR"), parameters
        )

    async def get_calendar_by_address(
        self,
        address: str,
        date: CalendarDateArg,
        params: Optional[Parameters] = None,
    ):
        """
        Get all prayer times for a specific calendar month/year from address.

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
                A month calendar if month parameter was given in date argument \
                otherwise a year calendar.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

            :exc:`~aladhan.exceptions.InternalServerError`
        """
        parameters = {"address": address}
        params = params or Parameters()
        parameters.update(params.as_dict)
        parameters.update(date.as_dict)
        return await self._get_timings(
            getattr(EndPoints, "HIJRI_" * date.hijri + "CALENDAR_BY_ADDRESS"),
            parameters,
        )

    async def get_calendar_by_city(
        self,
        city: str,
        country: str,
        date: CalendarDateArg,
        state: Optional[str] = None,
        params: Optional[Parameters] = None,
    ):
        """
        Get all prayer times for a specific calendar month/year from address.

        Parameters
        -----------
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
                A month calendar if month parameter was given in date argument \
                otherwise a year calendar.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

            :exc:`~aladhan.exceptions.InternalServerError`
        """
        parameters = {
            "city": city,
            "country": country,
            "state": state,
        }
        if state is None:
            del parameters["state"]
        params = params or Parameters()
        parameters.update(params.as_dict)
        parameters.update(date.as_dict)
        return await self._get_timings(
            getattr(EndPoints, "HIJRI_" * date.hijri + "CALENDAR_BY_CITY"),
            parameters,
        )

    @staticmethod
    def get_all_methods():
        """
        Gives all available prayer times calculation method.

        Returns
        -------
            dict[:class:`int`, :class:`Method`]
                A dict of available calculation method from 0 to 15.
        """
        return all_methods

    async def get_qibla(
        self, longitude: Union[int, float], latitude: Union[int, float]
    ):
        """
        Get the Qibla direction from a pair of coordinates.

        Returns
        -------
            :class:`Qibla`
                The qibla.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

            :exc:`~aladhan.exceptions.InternalServerError`

        *New in v0.1.3*
        """
        return Qibla(
            **(
                await self._get_res(
                    EndPoints.QIBLA + "/{}/{}".format(latitude, longitude), {}
                )
            )["data"]
        )

    async def get_asma(self, *n: int):
        """
        Returns a list of asma from giving numbers.

        Returns
        -------
            :class:`list` of :class:`Ism`
                A list of asma.

        Raises
        ------
            :exc:`~aladhan.exceptions.BadRequest`
                Invalid parameter was passed.

            :exc:`~aladhan.exceptions.InternalServerError`

        *New in v0.1.3*
        """

        assert n, "No arguments was passed."

        return [
            Ism(**d)
            for d in (
                await self._get_res(
                    EndPoints.ASMA_AL_HUSNA + "/" + ",".join(map(str, n)), {}
                )
            )["data"]
        ]

    async def get_all_asma(self):
        """
        Returns all 1-99 asma (allah names).

        Returns
        -------
            :class:`list` of :class:`Ism`
                A list of all asma.

        Raises
        ------
            :exc:`~aladhan.exceptions.InternalServerError`

        *New in v0.1.3*
        """
        return await self.get_asma(*range(1, 100))

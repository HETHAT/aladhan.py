from .exceptions import HTTPException
from .endpoints import *
from .types import (
    TimingsRes,
    CalendarRes,
    QiblaRes,
    AsmaRes,
    DateToDateRes,
    DateToCalendarRes,
)

import logging

log = logging.getLogger(__name__)


def missing_lib(msg):  # pragma: no cover
    def _():
        raise ImportError(msg)

    return _


try:
    from aiohttp import ClientSession
except ImportError:  # pragma: no cover
    log.warn("aiohttp library is not installed.")
    ClientSession = missing_lib(
        "`aiohttp` is a required library that is missing "
        "for asynchronous usage."
    )

try:
    from requests import Session
except ImportError:  # pragma: no cover
    log.warn("requests library is not installed.")
    Session = missing_lib(
        "`request` is a required library that is missing "
        "for synchronous usage."
    )

from typing import Awaitable, Union

TimingsR = Union[TimingsRes, Awaitable[TimingsRes]]
CalendarR = Union[CalendarRes, Awaitable[CalendarRes]]
QiblaR = Union[QiblaRes, Awaitable[QiblaRes]]
AsmaR = Union[AsmaRes, Awaitable[AsmaRes]]
DateR = Union[DateToDateRes, Awaitable[DateToDateRes]]
DTCR = Union[DateToCalendarRes, Awaitable[DateToCalendarRes]]

__all__ = ("HTTPClient",)


class HTTPClient:
    __slots__ = "requester", "request"

    def __init__(self, is_async: bool = False):
        self.requester = is_async and _AsyncRequester() or _SyncRequester()
        self.request = self.requester.request

    @property
    def is_async(self):
        return self.requester.is_async

    def close(self):
        log.debug("Closing session ...")
        return self.requester.session.close()  # this can be a coroutine

    # Timings
    def get_timings(self, date: str, params: dict) -> TimingsR:
        return self.request(TIMINGS + (date and "/" + date), params)

    def get_timings_by_address(self, date: str, params: dict) -> TimingsR:
        return self.request(TIMINGS_BY_ADDRESS + (date and "/" + date), params)

    def get_timings_by_city(self, date: str, params: dict) -> TimingsR:
        return self.request(TIMINGS_BY_CITY + (date and "/" + date), params)

    # Calendar
    def get_calendar(self, params: dict, hijri: bool = False) -> CalendarR:
        return self.request(hijri and HIJRI_CALENDAR or CALENDAR, params)

    def get_calendar_by_address(
        self, params: dict, hijri: bool = False
    ) -> CalendarR:
        return self.request(
            hijri and HIJRI_CALENDAR_BY_ADDRESS or CALENDAR_BY_ADDRESS, params
        )

    def get_calendar_by_city(
        self, params: dict, hijri: bool = False
    ) -> CalendarR:
        return self.request(
            hijri and HIJRI_CALENDAR_BY_CITY or CALENDAR_BY_CITY, params
        )

    # date converters
    def get_gregorian_from_hijri(self, params: dict) -> DateR:
        return self.request(G_TO_H, params)

    def get_hijri_from_gregorian(self, params: dict) -> DateR:
        return self.request(H_TO_G, params)

    def get_gregorian_calendar_from_hijri(self, params: tuple) -> DTCR:
        return self.request(G_TO_H_CALENDAR % params)

    def get_hijri_calendar_from_gregorian(self, params: tuple) -> DTCR:
        return self.request(H_TO_G_CALENDAR % params)

    def get_islamic_year_from_gregorian_for_ramadan(self, params: int) -> int:
        return self.request(ISLAMIC_YEAR_FROM_G_FOR_RAMADAN % params)

    # Others
    def get_asma(self, params: str) -> AsmaR:
        return self.request(ASMA_AL_HUSNA % params)

    def get_qibla(self, params: tuple) -> QiblaR:
        return self.request(QIBLA % params)


class _AsyncRequester:

    __slots__ = ("session",)

    def __init__(self):
        self.session: ClientSession = ClientSession()

    @property
    def is_async(self) -> bool:
        return True

    async def request(self, endpoint: str, params: dict = None):
        async with self.session.get(endpoint, params=params) as res:
            log.debug(
                "(GET)[%s status code] request to %s with %s",
                res.status,
                endpoint,
                params,
            )
            res = await res.json()

        if res["code"] != 200:  # something wrong
            raise HTTPException.from_res(res)
        return res["data"]


class _SyncRequester:

    __slots__ = ("session",)

    def __init__(self):
        self.session: Session = Session()

    @property
    def is_async(self) -> bool:
        return False

    def request(self, endpoint: str, params: dict = None):
        with self.session.get(endpoint, params=params) as res:
            log.debug(
                "(GET)[%s status code] request to %s with %s",
                res.status_code,
                endpoint,
                params,
            )
            res = res.json()

        if res["code"] != 200:  # something wrong
            raise HTTPException.from_res(res)
        return res["data"]

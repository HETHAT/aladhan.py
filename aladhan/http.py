from .exceptions import HTTPException
from .endpoints import *
from .types import (
    TimingsRes,
    CalendarRes,
    QiblaRes,
    AsmaRes,
)

import logging
log = logging.getLogger(__name__)


def missing_lib(msg):
    def _():
        raise ImportError(msg)
    return _

try:
    from aiohttp import ClientSession
except ImportError:
    log.warn("aiohttp library is not installed.")
    ClientSession = missing_lib(
        "`aiohttp` is a required library that is missing for asynchronous usage."
    )

try:
    from requests import Session
except ImportError:
    log.warn("requests library is not installed.")
    Session = missing_lib(
        "`request` is a required library that is missing for synchronous usage."
    )

from typing import Awaitable, Union

TimingsR = Union[TimingsRes, Awaitable[TimingsRes]]
CalendarR = Union[CalendarRes, Awaitable[CalendarRes]]
QiblaR = Union[QiblaRes, Awaitable[QiblaRes]]
AsmaR = Union[AsmaRes, Awaitable[AsmaRes]]

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

    def get_timings(self, date: str, params: dict) -> TimingsR:
        return self.request(TIMINGS + "/" + date, params)

    def get_timings_by_address(self, date: str, params: dict) -> TimingsR:
        return self.request(TIMINGS_BY_ADDRESS + "/" + date, params)

    def get_timings_by_city(self, date: str, params: dict) -> TimingsR:
        return self.request(TIMINGS_BY_CITY + "/" + date, params)

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

    def get_asma(self, query: str) -> AsmaR:
        return self.request(ASMA_AL_HUSNA + "/" + query, {})

    def get_qibla(self, latitude: str, longitude: str) -> QiblaR:
        return self.request(QIBLA + "/" + latitude + "/" + longitude, {})


class _AsyncRequester:

    __slots__ = ("session",)

    def __init__(self):
        self.session: ClientSession = ClientSession()

    @property
    def is_async(self) -> bool:
        return True

    async def request(self, endpoint: str, params: dict):
        async with self.session.get(endpoint, params=params) as res:
            log.debug("(GET)[%s status code] request to %s with %s", res.status, endpoint, params)
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

    def request(self, endpoint: str, params: dict):
        with self.session.get(endpoint, params=params) as res:
            log.debug("(GET)[%s status code] request to %s with %s", res.status_code, endpoint, params)
            res = res.json()

        if res["code"] != 200:  # something wrong
            raise HTTPException.from_res(res)
        return res["data"]

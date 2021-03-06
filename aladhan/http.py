from .exceptions import HTTPException
from .endpoints import *
from .types import (
    TimingsRes,
    CalendarRes,
    QiblaRes,
    AsmaRes,
    DateToDateRes,
    DateToCalendarRes,
    IslamicHolidaysRes,
    StatusR,
    SDR,
    IMR,
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

from typing import Awaitable as A, Union as U

TimingsR = U[TimingsRes, A[TimingsRes]]
CalendarR = U[CalendarRes, A[CalendarRes]]
QiblaR = U[QiblaRes, A[QiblaRes]]
AsmaR = U[AsmaRes, A[AsmaRes]]
DateR = U[DateToDateRes, A[DateToDateRes]]
DTCR = U[DateToCalendarRes, A[DateToCalendarRes]]
IHR = U[IslamicHolidaysRes, A[IslamicHolidaysRes]]
IntR = U[int, A[int]]
StrR = U[str, A[str]]
ListR = U[list, A[list]]


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

    # Next Prayer
    def get_next_prayer_by_address(self, date: str, params: dict):
        return self.request(
            NEXT_PRAYER_BY_ADDRESS + (date and "/" + date), params
        )

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
    def get_gregorian_from_hijri(self, **params) -> DateR:
        return self.request(H_TO_G, params)

    def get_hijri_from_gregorian(self, **params) -> DateR:
        return self.request(G_TO_H, params)

    def get_gregorian_calendar_from_hijri(self, *params) -> DTCR:
        return self.request(H_TO_G_CALENDAR % params)

    def get_hijri_calendar_from_gregorian(self, *params) -> DTCR:
        return self.request(G_TO_H_CALENDAR % params)

    def get_islamic_year_from_gregorian_for_ramadan(self, params: int) -> StrR:
        return self.request(ISLAMIC_YEAR_FROM_G_FOR_RAMADAN % params)

    # Current ...
    def get_current_time(self, **params) -> StrR:
        return self.request(CURRENT_TIME, params)

    def get_current_date(self, **params) -> StrR:
        return self.request(CURRENT_DATE, params)

    def get_current_timestamp(self, **params) -> StrR:
        return self.request(CURRENT_TIMESTAMP, params)

    def get_current_islamic_year(self, **params) -> StrR:
        return self.request(CURRENT_ISLAMIC_YEAR, params)

    def get_current_islamic_month(self, **params) -> IntR:
        return self.request(CURRENT_ISLAMIC_MONTH, params)

    # Holidays
    def get_next_hijri_holiday(self, **params) -> DateR:
        return self.request(NEXT_HIJRI_HOLIDAY, params)

    def get_hijri_holidays(self, *params) -> ListR:
        return self.request(HIJRI_HOLIDAYS % params)

    def get_islamic_holidays(self, *params) -> IHR:
        return self.request(ISLAMIC_HOLIDAYS_BY_H_YEAR % params)

    # Info
    def get_status(self) -> StatusR:
        return self.request(STATUS)

    def get_special_days(self) -> SDR:
        return self.request(SPECIAL_DAYS)

    def get_islamic_months(self) -> IMR:
        return self.request(ISLAMIC_MONTHS)

    # Others
    def get_asma(self, *params) -> AsmaR:
        return self.request(ASMA_AL_HUSNA % params)

    def get_qibla(self, *params) -> QiblaR:
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

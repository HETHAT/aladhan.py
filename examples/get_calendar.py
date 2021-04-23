import asyncio

from aladhan import (
    AsyncClient, Data, CalendarDateArg
)
from typing import List, Dict
from pprint import pprint


async def main():
    client = AsyncClient()

    # getting a year calendar
    data: Dict[str, List[Data]] = await client.get_calendar(
        longitude=69,
        latitude=42,
        date=CalendarDateArg(  # date arg in here is required
            year=2021,  # if month was not given then it will return a year calendar
        )
    )

    # getting a month calendar
    data: List[Data] = await client.get_calendar(
        longitude=69,
        latitude=42,
        date=CalendarDateArg(  # date arg in here is required
            year=2021,
            month=4
        )
    )

    # or you can get it using address
    data: List[Data] = await client.get_calendar_by_address(
        address="London",
        date=CalendarDateArg(  # date arg in here is required
            year=2021,
            month=4
        )
    )

    # or using city
    data: Data = await client.get_calendar_by_city(
        country="United Kingdom",
        city="London",
        date=CalendarDateArg(  # date arg in here is required
            year=2021,
            month=4
        )
    )

    pprint(data)

asyncio.run(main())

from typing import Dict, List

from aladhan import CalendarDateArg, Client, Timings


def main():
    client = Client()

    # getting a year calendar
    year_calendar: Dict[str, List[Timings]] = client.get_calendar(
        longitude=69,
        latitude=42,
        date=CalendarDateArg(  # date arg in here is required
            # if month was not given then return a year calendar
            year=2021,
        ),
    )

    # getting a month calendar
    month_calendar: List[Timings] = client.get_calendar(
        longitude=69,
        latitude=42,
        date=CalendarDateArg(
            year=2021, month=4
        ),  # date arg in here is required
    )

    # or you can get it using address
    month_calendar: List[Timings] = client.get_calendar_by_address(
        address="London",
        date=CalendarDateArg(
            year=2021, month=4
        ),  # date arg in here is required
    )

    # or using city
    month_calendar: List[Timings] = client.get_calendar_by_city(
        country="United Kingdom",
        city="London",
        date=CalendarDateArg(
            year=2021, month=4
        ),  # date arg in here is required
    )

    for timings in month_calendar:
        print(timings)
        print()

    client.close()


main()

import aladhan
from aladhan.exceptions import *

import datetime

# -------------- test_bases

TUNE = ("args", [[], [1], [10] * 9])
ERROR_METHOD = (["args", "expected"], [[("", 99, dict(isha="")), TypeError]])
TIMINGS_DATE = (
    ["arg", "expected"],
    [
        [datetime.datetime(2021, 5, 1), "01-05-2021"],
        [1619827200, "01-05-2021"],
        ["01-05-2021", "01-05-2021"],
    ],
)
ERROR_TIMINGS_DATE = (
    ["arg", "expected"],
    [["ERROR", ValueError]],
)
CALENDAR_DATE = (
    ["kwargs", "expected"],
    [
        [dict(year=2021), dict(year=2021, month=0, annual="true")],
        [dict(year=2021, month=None), dict(year=2021, month=0, annual="true")],
        [dict(year=2021, month=5), dict(year=2021, month=5, annual="false")],
        [dict(year=1442, hijri=True), dict(year=1442, month=0, annual="true")],
        [
            dict(year=1442, month=9, hijri=True),
            dict(year=1442, month=9, annual="false"),
        ],
    ],
)
ERROR_CALENDAR_DATE = (
    ["kwargs", "expected"],
    [[dict(), TypeError], [dict(year=2000, month=13), ValueError]],
)
PARAMETERS = (
    ["kwargs", "expected"],
    [
        [
            dict(),
            dict(
                method=2,
                tune="0,0,0,0,0,0,0,0,0",
                school=0,
                midnightMode=0,
                latitudeAdjustmentMethod=3,
                adjustment=0,
            ),
        ],
        [
            dict(
                method=aladhan.Method(
                    "", 99, params=dict(isha="null", maghrib=17, fajr=0)
                )
            ),
            99,
        ],
        [dict(method=aladhan.methods.MWL), 3],
        [dict(method=3), 3],
        [dict(method=15, shafaq="ahmer"), 15],
        [dict(tune=aladhan.Tune()), "0,0,0,0,0,0,0,0,0"],
        [dict(tune=None), "0,0,0,0,0,0,0,0,0"],
        [dict(tune=aladhan.Tune(1)), "1,0,0,0,0,0,0,0,0"],
        [dict(school=0), 0],
        [dict(school=1), 1],
        [dict(midnightMode=0), 0],
        [dict(midnightMode=1), 1],
        [dict(timezonestring="Africa/Algiers"), "Africa/Algiers"],
        [dict(latitudeAdjustmentMethod=1), 1],
        [dict(latitudeAdjustmentMethod=2), 2],
        [dict(latitudeAdjustmentMethod=3), 3],
        [dict(adjustment=17), 17],
    ],
)
ERROR_PARAMETERS = (
    ["kwargs", "expected"],
    [
        [dict(tune=aladhan.Tune("hi")), InvalidTune],
        [dict(tune=aladhan.Tune("0,0")), InvalidTune],
        [dict(tune=17), InvalidTune],
        [dict(method=99), InvalidMethod],
        [dict(method=17), InvalidMethod],
        [dict(school=2), InvalidSchool],
        [dict(midnightMode=3), InvalidMidnightMode],
        [dict(timezonestring="ta7ya ms3d"), InvalidTimezone],
        [dict(latitudeAdjustmentMethod=50), InvalidLatAdjMethod],
        [dict(adjustment=""), InvalidAdjustment],
        [
            dict(method=aladhan.methods.MOONSIGHTING, shafaq="Nonexistent"),
            InvalidShafaq,
        ],
    ],
)

# -------------- calendar_getters

GET_CALENDAR = (
    ["args", "kwargs", "expected"],
    [
        [(34, 4), dict(date=aladhan.CalendarDateArg(2021, 5)), list],
        [(34.69, 4.420), dict(date=aladhan.CalendarDateArg(2021)), dict],
        [
            (34, 4),
            dict(date=aladhan.CalendarDateArg(1442, 9, hijri=True)),
            list,
        ],
        [(34, 4), dict(date=aladhan.CalendarDateArg(1442, hijri=True)), dict],
        [
            (34, 4),
            dict(date=aladhan.CalendarDateArg(2021, 5), params=None),
            list,
        ],
        [
            (34, 4),
            dict(
                date=aladhan.CalendarDateArg(2021, 5),
                params=aladhan.Parameters(tune=aladhan.Tune(1)),
            ),
            list,
        ],
        [
            (34, 4),
            dict(
                date=aladhan.CalendarDateArg(1442, 9, hijri=True),
                params=aladhan.Parameters(tune=aladhan.Tune(1)),
            ),
            list,
        ],
    ],
)
GET_CALENDAR_BY_ADDRESS = (
    ["args", "kwargs", "expected"],
    [  # already mentioned above ...
        [["London"], dict(date=aladhan.CalendarDateArg(2021, 5)), list],
        [
            ["Djelfa"],
            dict(date=aladhan.CalendarDateArg(1442, hijri=True)),
            dict,
        ],
    ],
)
GET_CALENDAR_BY_CITY = (
    ["args", "kwargs", "expected"],
    [
        [
            ("London", "GB"),
            dict(state=None, date=aladhan.CalendarDateArg(2021, 5)),
            list,
        ],
        [
            ("London", "GB"),
            dict(
                state="Bexley", date=aladhan.CalendarDateArg(1444, hijri=True)
            ),
            dict,
        ],
    ],
)

# -------------- date_converters

GET_H_TO_G = (
    "args",
    [
        (aladhan.TimingsDateArg("25-01-1442"),),
        (aladhan.TimingsDateArg("25-01-1442"), 2),
    ],
)
GET_G_TO_H = (
    "args",
    [
        (aladhan.TimingsDateArg("25-01-2021"),),
        (aladhan.TimingsDateArg("25-01-2021"), 2),
    ],
)
GET_H_TO_G_CALENDAR = ("args", [(9, 1442), (9, 1442, 2)])
GET_G_TO_H_CALENDAR = ("args", [(1, 2021), (1, 2021, 2)])

# -------------- other_getters

GET_NEXT_PRAYER_BY_ADDRESS = (
    "args",
    [
        ("Djelfa, Messaad",),
        (
            "London",
            aladhan.TimingsDateArg("02-02-2020"),
            aladhan.Parameters(method=3),
        ),
    ],
)
GET_ASMA = ("args", [(1,), (1, 2, 3, 4), (1, 1, 1, 1, 1, 1, 2)])

# -------------- timings_getters

GET_TIMINGS = (
    ["args", "kwargs"],
    [
        [(34, 4), dict()],
        [(34.694, 3.5869), dict(date=None, params=None)],
        [(34, 4), dict(date=aladhan.TimingsDateArg("01-05-2021"))],
        [(34, 4), dict(params=aladhan.Parameters(adjustment=7))],
    ],
)
GET_TIMINGS_BY_ADDRESS = (
    ["args", "kwargs"],
    [
        [["London"], dict()],
        [["London"], dict(date=aladhan.TimingsDateArg())],
        [["London"], dict(params=aladhan.Parameters())],
    ],
)
GET_TIMINGS_BY_CITY = (
    ["args", "kwargs"],
    [
        [["London", "GB"], dict()],
        [["London", "GB", "Bexley"], dict()],
        [("London", "GB", None, None, None), dict()],
    ],
)

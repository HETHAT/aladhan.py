import pytest
import aladhan
import datetime
from aladhan.exceptions import *


@pytest.mark.asyncio
@pytest.fixture
async def data():
    data = (await aladhan.AsyncClient().get_timings(34, 4)).data
    assert (
        isinstance(data.meta, aladhan.Meta)
        and isinstance(data.timings, aladhan.Timings)
        and isinstance(data.date, aladhan.Date)
    )
    return data


@pytest.mark.parametrize("args", [[], [1], [10] * 9])
def test_tune(args):
    tune = aladhan.Tune(*args)
    assert isinstance(aladhan.Tune.from_str(tune.value), aladhan.Tune)


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        [("", 99, {"isha": ""}), TypeError],
    ],
)
def test_error_method(args, expected):
    try:
        aladhan.Method(*args)
    except expected:
        return
    raise RuntimeError()

@pytest.mark.parametrize(
    "arg", [datetime.datetime(2021, 5, 1), 1619827200, "01-05-2021"]
)
def test_timings_date(arg):
    assert aladhan.TimingsDateArg(arg).date == "01-05-2021"


@pytest.mark.parametrize(
    ["arg", "expected"],
    [["ERROR", ValueError]],
)
def test_error_timings_date(arg, expected):
    try:
        aladhan.TimingsDateArg(arg)
    except expected:
        return
    raise RuntimeError()


@pytest.mark.parametrize(
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
def test_calendar_date(kwargs, expected):
    assert aladhan.CalendarDateArg(**kwargs).as_dict == expected


@pytest.mark.parametrize(
    ["kwargs", "expected"],
    [[dict(), TypeError], [dict(year=2000, month=13), ValueError]],
)
def test_error_calendar_date(kwargs, expected):
    try:
        aladhan.CalendarDateArg(**kwargs)
    except expected:
        return
    raise RuntimeError()


@pytest.mark.parametrize(
    ["kwargs", "expected"],
    [
        [
            dict(),
            {
                "method": 2,
                "tune": "0,0,0,0,0,0,0,0,0",
                "school": 0,
                "midnightMode": 0,
                "latitudeAdjustmentMethod": 3,
                "adjustment": 0,
            },
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
def test_default_args(kwargs, expected):
    dct = aladhan.DefaultArgs(**kwargs).as_dict
    kwargs = kwargs.keys()
    assert dct.get(kwargs and tuple(kwargs)[0] or None, dct) == expected


@pytest.mark.parametrize(
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
        [dict(adjustment=""), InvalidAdjustment]
    ],
)
def test_error_default_args(kwargs, expected):
    try:
        aladhan.DefaultArgs(**kwargs)
    except expected:
        return
    raise RuntimeError()


def test_meta(data):
    assert isinstance(data.meta.default_args, aladhan.DefaultArgs)


@pytest.mark.asyncio
async def test_timings(data):
    for _ in (data.timings.prayers_only.values(), data.timings):
        for prayer in _:
            assert (
                isinstance(prayer, aladhan.Prayer)
                and isinstance(prayer.remaining, datetime.timedelta)
                and isinstance(prayer.remaining_utc, (datetime.timedelta, None))
            )

    np = await data.timings.next_prayer()
    assert isinstance(np, aladhan.Prayer)
    #  you should not do this
    assert isinstance(
        aladhan.Prayer("Test", "11:11", data.timings).remaining,
        datetime.timedelta,
    )

import pytest
import aladhan


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        [(34, 4), {"date": aladhan.CalendarDateArg(2021, 5)}, list],
        [(34, 4), {"date": aladhan.CalendarDateArg(2021)}, dict],
        [
            (34, 4),
            {"date": aladhan.CalendarDateArg(1442, 9, hijri=True)},
            list,
        ],
        [(34, 4), {"date": aladhan.CalendarDateArg(1442, hijri=True)}, dict],
        [
            (34.69, 4.420),
            {
                "date": aladhan.CalendarDateArg(2021, 5),
                "params": None,
            },
            list,
        ],
        [
            (34, 4),
            {
                "date": aladhan.CalendarDateArg(2021, 5),
                "params": aladhan.Parameters(tune=aladhan.Tune(1)),
            },
            list,
        ],
        [
            (34, 4),
            {
                "date": aladhan.CalendarDateArg(1442, 9, hijri=True),
                "params": aladhan.Parameters(tune=aladhan.Tune(1)),
            },
            list,
        ],
    ],
)
async def test_calendar(client, args, kwargs, expected):
    ts = await client.get_calendar(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        [("London",), {"date": aladhan.CalendarDateArg(2021)}, dict],
        [
            ("London",),
            {"date": aladhan.CalendarDateArg(1442, 9, hijri=True)},
            list,
        ],
        [
            ("London",),
            {"date": aladhan.CalendarDateArg(1442, hijri=True)},
            dict,
        ],
        [
            ("London",),
            {
                "date": aladhan.CalendarDateArg(2021, 5),
                "params": aladhan.Parameters(tune=aladhan.Tune(1)),
            },
            list,
        ],
        [
            ("London",),
            {
                "date": aladhan.CalendarDateArg(1442, 9, hijri=True),
                "params": aladhan.Parameters(tune=aladhan.Tune(1)),
            },
            list,
        ],
    ],
)
async def test_calendar_by_address(client, args, kwargs, expected):
    ts = await client.get_calendar_by_address(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        [("London", "GB"), {"date": aladhan.CalendarDateArg(2021)}, dict],
        [
            ("London", "GB"),
            {"date": aladhan.CalendarDateArg(2021), "state": "Bexley"},
            dict,
        ],
        [
            ("London", "GB"),
            {
                "date": aladhan.CalendarDateArg(2021),
                "state": None,
                "params": None,
            },
            dict,
        ],
        [("London", "GB"), {"date": aladhan.CalendarDateArg(2021)}, dict],
        [
            ("London", "GB"),
            {"date": aladhan.CalendarDateArg(1442, 9, hijri=True)},
            list,
        ],
        [
            ("London", "GB"),
            {"date": aladhan.CalendarDateArg(1442, hijri=True)},
            dict,
        ],
        [
            ("London", "GB"),
            {
                "date": aladhan.CalendarDateArg(2021, 5),
                "params": aladhan.Parameters(tune=aladhan.Tune(1)),
            },
            list,
        ],
        [
            ("London", "GB"),
            {
                "date": aladhan.CalendarDateArg(1442, 9, hijri=True),
                "params": aladhan.Parameters(tune=aladhan.Tune(1)),
            },
            list,
        ],
    ],
)
async def test_calendar_by_city(client, args, kwargs, expected):
    ts = await client.get_calendar_by_city(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)

import pytest
import aladhan


@pytest.mark.asyncio
@pytest.fixture
async def client():
    return aladhan.AsyncClient()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        [(34, 4), {"date": aladhan.CalendarDateArg(2021, 5)}, list],
        [(34, 4), {"date": aladhan.CalendarDateArg(2021)}, dict],
        [(34, 4), {"date": aladhan.CalendarDateArg(1442, 9, hijri=True)}, list],
        [(34, 4), {"date": aladhan.CalendarDateArg(1442, hijri=True)}, dict],
        [
            (34, 4),
            {
                "date": aladhan.CalendarDateArg(2021, 5),
                "defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1)),
            },
            list,
        ],
        [
            (34, 4),
            {
                "date": aladhan.CalendarDateArg(1442, 9, hijri=True),
                "defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1)),
            },
            list,
        ],
    ],
)
async def test_calendar(client, args, kwargs, expected):
    ts = await client.get_calendar(*args, **kwargs)
    assert isinstance(ts, expected)


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
                "defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1)),
            },
            list,
        ],
        [
            ("London",),
            {
                "date": aladhan.CalendarDateArg(1442, 9, hijri=True),
                "defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1)),
            },
            list,
        ],
    ],
)
async def test_calendar_by_address(client, args, kwargs, expected):
    ts = await client.get_calendar_by_address(*args, **kwargs)
    assert isinstance(ts, expected)


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
                "defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1)),
            },
            list,
        ],
        [
            ("London", "GB"),
            {
                "date": aladhan.CalendarDateArg(1442, 9, hijri=True),
                "defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1)),
            },
            list,
        ],
    ],
)
async def test_calendar_by_city(client, args, kwargs, expected):
    ts = await client.get_calendar_by_city(*args, **kwargs)
    assert isinstance(ts, expected)

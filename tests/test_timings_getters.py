import pytest
import aladhan


@pytest.mark.asyncio
@pytest.fixture
async def client():
    return aladhan.AsyncClient()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [(34, 4), {}],
        [(34, 4), {"date": aladhan.TimingsDateArg("01-05-2021")}],
        [(34, 4), {"defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1))}],
    ],
)
async def test_timings(client, args, kwargs):
    ts = await client.get_timings(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        [("London",), {}, False],
        [("London",), {"date": aladhan.TimingsDateArg("01-05-2021")}, False],
        [
            ("London",),
            {"defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1))},
            False,
        ],
        [("ThisWillErrorLmaoooooo",), {}, Exception],
    ],
)
async def test_timings_by_address(client, args, kwargs, expected):
    if expected:
        bonk = False
        try:
            await client.get_timings_by_address(*args, **kwargs)
        except expected:
            bonk = True
        assert bonk
    else:
        ts = await client.get_timings_by_address(*args, **kwargs)
        assert isinstance(ts, aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        [("London", "GB"), {}, False],
        [("London", "GB", "Bexley"), {}, False],
        [
            ("London", "GB"),
            {"date": aladhan.TimingsDateArg("01-05-2021")},
            False,
        ],
        [
            ("London", "GB"),
            {"defaults": aladhan.DefaultArgs(tune=aladhan.Tune(1))},
            False,
        ],
        [("", ""), {}, Exception],
    ],
)
async def test_timings_by_city(client, args, kwargs, expected):
    if expected:
        bonk = False
        try:
            await client.get_timings_by_city(*args, **kwargs)
        except expected:
            bonk = True
        assert bonk
    else:
        ts = await client.get_timings_by_city(*args, **kwargs)
        assert isinstance(ts, aladhan.Timings)

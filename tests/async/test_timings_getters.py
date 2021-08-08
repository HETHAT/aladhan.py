import pytest
import aladhan


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [(34, 4), {}],
        [(34.694, 3.5869), {"date": None, "params": None}],
        [(34, 4), {"date": aladhan.TimingsDateArg("01-05-2021")}],
        [(34, 4), {"params": aladhan.Parameters(tune=aladhan.Tune(1))}],
    ],
)
async def test_timings(client, args, kwargs):
    ts = await client.get_timings(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [("London",), {}],
        [("London",), {"date": aladhan.TimingsDateArg("01-05-2021")}],
        [
            ("London",),
            {"params": aladhan.Parameters(tune=aladhan.Tune(1))},
        ],
    ],
)
async def test_timings_by_address(client, args, kwargs):
    ts = await client.get_timings_by_address(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [("London", "GB"), {}],
        [("London", "GB", "Bexley"), {}],
        [("London", "GB", None, None, None), {}],
        [
            ("London", "GB"),
            {"date": aladhan.TimingsDateArg("01-05-2021")},
        ],
        [
            ("London", "GB"),
            {"params": aladhan.Parameters(tune=aladhan.Tune(1))},
        ],
    ],
)
async def test_timings_by_city(client, args, kwargs):
    ts = await client.get_timings_by_city(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)

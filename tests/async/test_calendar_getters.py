import pytest

from ..pms import *  # include aladhan module


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_CALENDAR)
async def test_calendar(client, args, kwargs, expected):
    ts = await client.get_calendar(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_CALENDAR_BY_ADDRESS)
async def test_calendar_by_address(client, args, kwargs, expected):
    ts = await client.get_calendar_by_address(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_CALENDAR_BY_CITY)
async def test_calendar_by_city(client, args, kwargs, expected):
    ts = await client.get_calendar_by_city(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)

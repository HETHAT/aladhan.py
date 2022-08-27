import pytest

from ..pms import *  # include aladhan module


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_TIMINGS)
async def test_timings(client, args, kwargs):
    ts = await client.get_timings(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_TIMINGS_BY_ADDRESS)
async def test_timings_by_address(client, args, kwargs):
    ts = await client.get_timings_by_address(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_TIMINGS_BY_CITY)
async def test_timings_by_city(client, args, kwargs):
    ts = await client.get_timings_by_city(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)

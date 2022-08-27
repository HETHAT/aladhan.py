import pytest

from ..pms import *  # include aladhan module


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_H_TO_G)
async def test_h_to_g(client, args):
    assert isinstance(
        await client.get_gregorian_from_hijri(*args), aladhan.Date
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_G_TO_H)
async def test_g_to_h(client, args):
    assert isinstance(
        await client.get_hijri_from_gregorian(*args), aladhan.Date
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_H_TO_G_CALENDAR)
async def test_h_to_g_calendar(client, args):
    r = await client.get_gregorian_calendar_from_hijri(*args)
    assert isinstance(r, list) and isinstance(r[0], aladhan.Date)


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_G_TO_H_CALENDAR)
async def test_g_to_h_calendar(client, args):
    r = await client.get_hijri_calendar_from_gregorian(*args)
    assert isinstance(r, list) and isinstance(r[0], aladhan.Date)


@pytest.mark.asyncio
async def test_islamic_year(client):
    r = await client.get_islamic_year_from_gregorian_for_ramadan(2021)
    assert r == 1442

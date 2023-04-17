import pytest

from ..pms import *  # includes aladhan module


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_NEXT_PRAYER_BY_ADDRESS)
async def test_next_prayer_by_address(client, args):
    p = await client.get_next_prayer_by_address(*args)
    assert isinstance(p, aladhan.Prayer)
    assert isinstance(p.data, aladhan.NextPrayerData)


@pytest.mark.asyncio
async def test_qibla(client):
    q = await client.get_qibla(3, 34)
    assert isinstance(q, aladhan.Qibla)


@pytest.mark.asyncio
@pytest.mark.parametrize(*GET_ASMA)
async def test_asma(client, args):
    asma = await client.get_asma(*args)
    assert asma and isinstance(asma, list) and isinstance(asma[0], aladhan.Ism)


@pytest.mark.asyncio
async def test_all_asma(client):
    asma = await client.get_all_asma()
    assert (
        len(asma) == 99
        and isinstance(asma, list)
        and isinstance(asma[0], aladhan.Ism)
    )


def test_all_methods(client):
    methods = client.get_all_methods()
    for i, x in methods.items():
        assert isinstance(i, int) and isinstance(x, aladhan.methods.Method)


@pytest.mark.asyncio
async def test_the_rest(client):
    # assert (await client.get_status()).get("status") == "alive"
    assert list((await client.get_special_days())[0]) == [
        "month",
        "day",
        "name",
    ]
    assert list((await client.get_islamic_months())["1"]) == [
        "number",
        "en",
        "ar",
    ]

import pytest
import aladhan


@pytest.mark.asyncio
@pytest.fixture
async def client():
    async with aladhan.Client(True) as client:
        yield client


@pytest.mark.asyncio
async def test_qibla(client):
    q = await client.get_qibla(3, 34)
    assert isinstance(q, aladhan.Qibla)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["args"], [[(1,)], [(1, 2, 3, 4)], [(1, 1, 1, 1, 1, 1, 2)]]
)
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

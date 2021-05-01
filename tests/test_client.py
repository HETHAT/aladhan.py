import pytest
import aladhan


@pytest.mark.asyncio
@pytest.fixture
async def client():
    return aladhan.AsyncClient()


def test_all_methods(client):
    methods = client.get_all_methods()
    for i, x in methods.items():
        assert isinstance(i, int) and isinstance(x, aladhan.methods.Method)

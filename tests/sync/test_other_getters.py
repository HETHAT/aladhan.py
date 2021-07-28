import pytest
import aladhan


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


def test_qibla(client):
    q = client.get_qibla(3, 34)
    assert isinstance(q, aladhan.Qibla)


@pytest.mark.parametrize(
    ["args"], [[(1,)], [(1, 2, 3, 4)], [(1, 1, 1, 1, 1, 1, 2)]]
)
def test_asma(client, args):
    asma = client.get_asma(*args)
    assert asma and isinstance(asma, list) and isinstance(asma[0], aladhan.Ism)


def test_all_asma(client):
    asma = client.get_all_asma()
    assert (
        len(asma) == 99
        and isinstance(asma, list)
        and isinstance(asma[0], aladhan.Ism)
    )


def test_all_methods(client):
    methods = client.get_all_methods()
    for i, x in methods.items():
        assert isinstance(i, int) and isinstance(x, aladhan.methods.Method)

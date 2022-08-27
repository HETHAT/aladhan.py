import pytest

import aladhan
from ..pms import *  # includes aladhan module


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


@pytest.mark.parametrize(*GET_NEXT_PRAYER_BY_ADDRESS)
def test_next_prayer_by_address(client, args):
    p = client.get_next_prayer_by_address(*args)
    assert isinstance(p, aladhan.Prayer)
    assert isinstance(p.data, aladhan.NextPrayerData)


def test_qibla(client):
    q = client.get_qibla(3, 34)
    assert isinstance(q, aladhan.Qibla)


@pytest.mark.parametrize(*GET_ASMA)
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


def test_the_rest(client):
    assert client.get_status().get("memcached") == "OK"
    assert list(client.get_special_days()[0]) == ["month", "day", "name"]
    assert list(client.get_islamic_months()["1"]) == ["number", "en", "ar"]

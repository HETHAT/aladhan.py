import pytest

from ..pms import *  # includes aladhan module


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


@pytest.mark.parametrize(*GET_TIMINGS)
def test_timings(client, args, kwargs):
    ts = client.get_timings(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.parametrize(*GET_TIMINGS_BY_ADDRESS)
def test_timings_by_address(client, args, kwargs):
    ts = client.get_timings_by_address(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.parametrize(*GET_TIMINGS_BY_CITY)
def test_timings_by_city(client, args, kwargs):
    ts = client.get_timings_by_city(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)

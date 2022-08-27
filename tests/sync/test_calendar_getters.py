import pytest

from ..pms import *  # includes aladhan module


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


@pytest.mark.parametrize(*GET_CALENDAR)
def test_calendar(client, args, kwargs, expected):
    ts = client.get_calendar(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)


@pytest.mark.parametrize(*GET_CALENDAR_BY_ADDRESS)
def test_calendar_by_address(client, args, kwargs, expected):
    ts = client.get_calendar_by_address(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)


@pytest.mark.parametrize(*GET_CALENDAR_BY_CITY)
def test_calendar_by_city(client, args, kwargs, expected):
    ts = client.get_calendar_by_city(*args, **kwargs)
    assert isinstance(ts, expected)
    assert isinstance(expected == list and ts[0] or ts["1"][0], aladhan.Timings)

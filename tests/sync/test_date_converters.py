import pytest

from ..pms import *  # includes aladhan module


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


@pytest.mark.parametrize(*GET_H_TO_G)
def test_h_to_g(client, args):
    assert isinstance(client.get_gregorian_from_hijri(*args), aladhan.Date)


@pytest.mark.parametrize(*GET_G_TO_H)
def test_g_to_h(client, args):
    assert isinstance(client.get_hijri_from_gregorian(*args), aladhan.Date)


@pytest.mark.parametrize(*GET_H_TO_G_CALENDAR)
def test_h_to_g_calendar(client, args):
    r = client.get_gregorian_calendar_from_hijri(*args)
    assert isinstance(r, list) and isinstance(r[0], aladhan.Date)


@pytest.mark.parametrize(*GET_G_TO_H_CALENDAR)
def test_g_to_h_calendar(client, args):
    r = client.get_hijri_calendar_from_gregorian(*args)
    assert isinstance(r, list) and isinstance(r[0], aladhan.Date)


def test_islamic_year(client):
    r = client.get_islamic_year_from_gregorian_for_ramadan(2021)
    assert r == 1442

import pytest
import aladhan


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


@pytest.mark.parametrize(
    "args",
    [
        (aladhan.TimingsDateArg("25-01-1442"),),
        (aladhan.TimingsDateArg("25-01-1442"), 2),
    ],
)
def test_h_to_g(client, args):
    assert isinstance(client.get_gregorian_from_hijri(*args), aladhan.Date)


@pytest.mark.parametrize(
    "args",
    [
        (aladhan.TimingsDateArg("25-01-2021"),),
        (aladhan.TimingsDateArg("25-01-2021"), 2),
    ],
)
def test_g_to_h(client, args):
    assert isinstance(client.get_hijri_from_gregorian(*args), aladhan.Date)


@pytest.mark.parametrize("args", [(9, 1442), (9, 1442, 2)])
def test_h_to_g_calendar(client, args):
    r = client.get_gregorian_calendar_from_hijri(*args)
    assert isinstance(r, list) and isinstance(r[0], aladhan.Date)


@pytest.mark.parametrize("args", [(1, 2021), (1, 2021, 2)])
def test_g_to_h_calendar(client, args):
    r = client.get_hijri_calendar_from_gregorian(*args)
    assert isinstance(r, list) and isinstance(r[0], aladhan.Date)


def test_islamic_year(client):
    r = client.get_islamic_year_from_gregorian_for_ramadan(2021)
    assert r == 1442

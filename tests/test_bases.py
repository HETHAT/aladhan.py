import pytest

from .pms import *  # aladhan is imported from here


@pytest.fixture
def data():
    data = (aladhan.Client().get_timings(34, 4)).data
    assert (
        isinstance(data.meta, aladhan.Meta)
        and isinstance(data.timings, aladhan.Timings)
        and isinstance(data.date, aladhan.Date)
    )
    return data


@pytest.mark.parametrize(*TUNE)
def test_tune(args):
    tune = aladhan.Tune(*args)
    assert isinstance(aladhan.Tune.from_str(tune.value), aladhan.Tune)


@pytest.mark.parametrize(*ERROR_METHOD)
def test_error_method(args, expected):
    with pytest.raises(expected):
        aladhan.Method(*args)


@pytest.mark.parametrize(*TIMINGS_DATE)
def test_timings_date(arg, expected):
    assert aladhan.TimingsDateArg(arg).date == expected


@pytest.mark.parametrize(*ERROR_TIMINGS_DATE)
def test_error_timings_date(arg, expected):
    with pytest.raises(expected):
        aladhan.TimingsDateArg(arg)


@pytest.mark.parametrize(*CALENDAR_DATE)
def test_calendar_date(kwargs, expected):
    assert aladhan.CalendarDateArg(**kwargs).as_dict == expected


@pytest.mark.parametrize(*ERROR_CALENDAR_DATE)
def test_error_calendar_date(kwargs, expected):
    with pytest.raises(expected):
        aladhan.CalendarDateArg(**kwargs)


@pytest.mark.parametrize(*PARAMETERS)
def test_parameters(kwargs, expected):
    dct = aladhan.Parameters(**kwargs).as_dict
    kwargs = kwargs.keys()
    assert dct.get(kwargs and tuple(kwargs)[0] or None, dct) == expected


@pytest.mark.parametrize(*ERROR_PARAMETERS)
def test_error_parameters(kwargs, expected):
    with pytest.raises(expected):
        aladhan.Parameters(**kwargs)


def test_meta(data):
    assert isinstance(data.meta.parameters, aladhan.Parameters)


def test_timings(data):
    for _ in (data.timings.prayers_only.values(), data.timings):
        for prayer in _:
            assert (
                isinstance(prayer, aladhan.Prayer)
                and isinstance(prayer.remaining, datetime.timedelta)
                and isinstance(prayer.remaining_utc, (datetime.timedelta, None))
            )

    np = data.timings.next_prayer()
    assert np is None or isinstance(np, aladhan.Prayer)

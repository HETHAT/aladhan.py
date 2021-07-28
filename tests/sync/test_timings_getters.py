import pytest
import aladhan


@pytest.fixture
def client():
    with aladhan.Client() as client:
        yield client


@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [(34, 4), {}],
        [(34.694, 3.5869), {"date": None, "params": None}],
        [(34, 4), {"date": aladhan.TimingsDateArg("01-05-2021")}],
        [(34, 4), {"params": aladhan.Parameters(tune=aladhan.Tune(1))}],
    ],
)
def test_timings(client, args, kwargs):
    ts = client.get_timings(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [("London",), {}],
        [("London",), {"date": aladhan.TimingsDateArg("01-05-2021")}],
        [
            ("London",),
            {"params": aladhan.Parameters(tune=aladhan.Tune(1))},
        ],
    ],
)
def test_timings_by_address(client, args, kwargs):
    ts = client.get_timings_by_address(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [[("ThisShouldError",), {}, Exception], [("",), {}, Exception]],
)
def test_error_timings_by_address(args, kwargs, expected):
    try:
        client.get_timings_by_address(*args, **kwargs)
    except expected:
        return
    raise RuntimeError()


@pytest.mark.parametrize(
    ["args", "kwargs"],
    [
        [("London", "GB"), {}],
        [("London", "GB", "Bexley"), {}],
        [("London", "GB", None, None, None), {}],
        [
            ("London", "GB"),
            {"date": aladhan.TimingsDateArg("01-05-2021")},
        ],
        [
            ("London", "GB"),
            {"params": aladhan.Parameters(tune=aladhan.Tune(1))},
        ],
    ],
)
def test_timings_by_city(client, args, kwargs):
    ts = client.get_timings_by_city(*args, **kwargs)
    assert isinstance(ts, aladhan.Timings)


@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [[("", ""), {}, Exception], [("Doesn't", "Exist"), {}, Exception]],
)
def test_error_timings_by_city(args, kwargs, expected):
    try:
        client.get_timings_by_city(*args, **kwargs)
    except expected:
        return
    raise RuntimeError()

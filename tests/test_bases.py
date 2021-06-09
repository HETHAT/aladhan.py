import pytest
import aladhan
import datetime


@pytest.mark.asyncio
@pytest.fixture
async def data():
    dt = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    return (
        await aladhan.AsyncClient().get_timings(
            34, 4, date=aladhan.TimingsDateArg(dt)
        )
    ).data


def test_tune():
    tune = aladhan.Tune()
    assert isinstance(aladhan.Tune.from_str(tune.value), aladhan.Tune)


def test_date_args():
    for i in (datetime.datetime(2021, 5, 1), 1619827200, "01-05-2021"):
        assert aladhan.TimingsDateArg(i).date == "01-05-2021"
    # calendar date arg already tested


def test_meta(data):
    assert isinstance(data.meta.default_args, aladhan.DefaultArgs)


@pytest.mark.asyncio
async def test_timings(data):
    for _ in (data.timings.prayers_only, data.timings.as_dict):
        for prayer in _.values():
            assert (
                isinstance(prayer, aladhan.Prayer)
                and isinstance(prayer.remaining, datetime.timedelta)
                and isinstance(prayer.remaining_utc, (datetime.timedelta, None))
            )

    np = await data.timings.next_prayer()
    assert isinstance(np, aladhan.Prayer)
    #  you should not do this
    assert isinstance(
        aladhan.Prayer("Test", "11:11", data.timings).remaining,
        datetime.timedelta,
    )

import pytest

import aladhan


@pytest.mark.asyncio
async def test_holidays():
    async with aladhan.Client(True) as client:
        assert await client.get_hijri_holidays(10, 12) == [
            "Eid-ul-Adha",
            "Hajj",
        ]
        assert isinstance(await client.get_next_hijri_holiday(), aladhan.Date)
        _ = await client.get_islamic_holidays(1442)
        assert isinstance(_, list), isinstance(_[0], aladhan.Date)

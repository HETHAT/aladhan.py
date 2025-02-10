import pytest

import aladhan


@pytest.mark.asyncio
async def test_current():
    async with aladhan.Client(True) as client:
        assert isinstance(await client.get_current_time("Africa/Algiers"), str)
        assert isinstance(await client.get_current_date("Africa/Algiers"), str)
        assert isinstance(
            await client.get_current_timestamp("Africa/Algiers"), int
        )
        assert isinstance(await client.get_current_islamic_year(), int)
        assert isinstance(await client.get_current_islamic_month(), int)

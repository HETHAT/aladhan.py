import asyncio

from aladhan import AsyncClient, Timings


async def main():
    client = AsyncClient()
    # you can get by coordinates
    timings: Timings = await client.get_timings(longitude=69, latitude=42)
    # or by address
    timings: Timings = await client.get_timings_by_address(address="London")

    next_prayer = await timings.next_prayer()
    print(next_prayer, "remaining:", next_prayer.remaining)
    print(next_prayer, "remaining for utc:", next_prayer.remaining_utc)


asyncio.run(main())

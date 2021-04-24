import asyncio

from aladhan import AsyncClient, Timings


async def main():
    client = AsyncClient()
    # getting data
    timings: Timings = await client.get_timings(longitude=69, latitude=42)

    # only Timings obj is required to get next prayer
    next_prayer = await timings.next_prayer()
    print(next_prayer)
    print(next_prayer.remaining)


asyncio.run(main())

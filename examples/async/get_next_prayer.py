import asyncio

from aladhan import Client, Timings


async def main():
    client = Client(is_async=True)
    # you can get by coordinates
    timings: Timings = await client.get_timings(longitude=69, latitude=42)
    # or by address
    timings: Timings = await client.get_timings_by_address(address="London")

    next_prayer = timings.next_prayer()
    print(next_prayer, "remaining:", next_prayer.remaining)
    print(next_prayer, "remaining for utc:", next_prayer.remaining_utc)

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
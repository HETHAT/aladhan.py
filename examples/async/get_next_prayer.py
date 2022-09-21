import asyncio

from aladhan import Client


async def main():
    client = Client(is_async=True)
    next_prayer = await client.get_next_prayer_by_address(address="London")
    print(next_prayer, "remaining:", next_prayer.remaining)

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

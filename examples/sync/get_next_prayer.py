from aladhan import Client, Timings


def main():
    client = Client()
    # you can get by coordinates
    timings: Timings = client.get_timings(longitude=69, latitude=42)
    # or by address
    timings: Timings = client.get_timings_by_address(address="London")

    next_prayer = timings.next_prayer()
    print(next_prayer, "remaining:", next_prayer.remaining)
    print(next_prayer, "remaining for utc:", next_prayer.remaining_utc)

    client.close()


main()

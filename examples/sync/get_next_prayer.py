from aladhan import Client


def main():
    client = Client()
    next_prayer = client.get_next_prayer_by_address(address="London")

    print(next_prayer, "remaining:", next_prayer.remaining)
    print(next_prayer, "remaining for utc:", next_prayer.remaining_utc)

    client.close()


main()

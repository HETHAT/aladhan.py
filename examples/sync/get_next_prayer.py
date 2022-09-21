from aladhan import Client


def main():
    client = Client()
    next_prayer = client.get_next_prayer_by_address(address="London")

    print(next_prayer, "remaining:", next_prayer.remaining)
    client.close()


main()

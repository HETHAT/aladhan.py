from aladhan import (
    Client,
    TimingsDateArg,
    Parameters,
    methods,
    Tune,
    Schools,
    MidnightModes,
    LatitudeAdjustmentMethods,
    Timings,
)


def main():
    client = Client()

    timings: Timings = client.get_timings(longitude=69, latitude=42)
    # or even specify more
    timings: Timings = client.get_timings(
        longitude=69,
        latitude=42,
        date=TimingsDateArg(
            # it also accepts an int (unix time) and datetime() obj
            "23-04-2021"
        ),
        params=Parameters(
            # methods.all_methods to see all available methods
            method=methods.ISNA,
            tune=Tune(
                Asr=+10,
                # and other params ...
            ),
            school=Schools.SHAFI,
            midnightMode=MidnightModes.JAFARI,
            latitudeAdjustmentMethod=LatitudeAdjustmentMethods.ANGLE_BASED,
            adjustment=1,
        ),
    )
    # or you can get it using address
    timings: Timings = client.get_timings_by_address(address="London")

    # or using city
    timings: Timings = client.get_timings_by_city(
        country="United Kingdom", city="London"
    )

    for k, v in timings.prayers_only.items():
        print(f"{k} at {v.time}, {v.remaining} left")

    client.close()


main()

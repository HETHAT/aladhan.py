.. currentmodule:: aladhan

.. _quickstart:

Quickstart
==========

To start we are going to import ``aladhan`` and ``asyncio``, then we are going
to define a client in an asynchronous function.

.. code-block:: py

    import aladhan
    import asyncio

    async def main():
        client = aladhan.AsyncClient()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Of course this will do nothing but we are going to use the client soon.

.. _ref-timings:

Timings (Day Timings)
---------------------

Want to get your prayer times ? you can use :meth:`AsyncClient.get_timings`  which will return
a :class:`Timings` object:

.. code-block:: py

    import aladhan
    import asyncio

    async def main():
        client = aladhan.AsyncClient()
        timings: aladhan.Timings = await client.get_timings(latitude=34, longitude=3)
        for prayer in timings:
            print(prayer.name, prayer.time)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Output would be

.. code-block::

    Imsak 2021-06-08 04:03:00
    Fajr 2021-06-08 04:13:00
    Sunrise 2021-06-08 05:36:00
    Dhuhr 2021-06-08 12:47:00
    Asr 2021-06-08 16:32:00
    Sunset 2021-06-08 19:58:00
    Maghrib 2021-06-08 19:58:00
    Isha 2021-06-08 21:22:00
    Midnight 2021-06-08 00:47:00

Time's date is set to current date by default if you want to change that you can
use :meth:`TimingsDateArg`:

.. code-block:: py

    timings: aladhan.Timings = await client.get_timings(
        latitude=34,
        longitude=3,
        # TimingsDateArg takes one argument and it can
        # be a string in a DD-MM-YYYY format or
        # or a datetime.datetime obj or
        # or an int representing a unix date
        date=aladhan.TimingsDateArg("28-05-2022")
    )

What if you don't like using coordinates ?
You can use :meth:`AsyncClient.get_timings_by_address`

.. _ref-ts-by-address:

.. code-block:: py

    timings: aladhan.Timings = await client.get_timings_by_address(address="United Kingdom, London")

or use :meth:`AsyncClient.get_timings_by_city`

.. code-block:: py

    timings: aladhan.Timings = await client.get_timings_by_city(country="United Kingdom", city="London")

You can configure more using :class:`Parameters`, look into :ref:`ref-conf`.

Calendar Timings
----------------
If you want to get the prayer times of more than just 1 day you
can use :meth:`AsyncClient.get_calendar`.

.. code-block:: py

    import aladhan
    import asyncio
    import typing

    async def main():
        client = aladhan.AsyncClient()
        month_calendar: typing.List[aladhan.Timings] = await client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(
                year=2021,
                month=1
            )
        )
        for timings in month_calendar:
            print(timings)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

``month`` argument for :class:`CalendarDateArg` is optional, and by not providing it
or passing 0, it will return a *year calendar*, a dict of strings ("1",...,"12")
and list of :class:`Timings` object.

.. code-block:: py

    year_calendar: typing.Dict[str, aladhan.Timings] = await client.get_calendar(
        latitude=34,
        longitude=3,
        date=aladhan.CalendarDateArg(year=2021)
    )

you can also use *hijri* date by setting ``hijri`` argument to ``True``

.. code-block:: py

    year_calendar: typing.Dict[str, aladhan.Timings] = await client.get_calendar(
        latitude=34,
        longitude=3,
        date=aladhan.CalendarDateArg(year=1442, hijri=True)  # month arg still can be used
        )

And as for using coordinates, you can use address using :meth:`AsyncClient.get_calendar_by_address`
or city/country using :meth:`AsyncClient.get_calendar_by_city`,
it is the same way as :ref:`day timings <ref-ts-by-address>`.

.. _ref-conf:

Configuring
-----------

All previous getters (day timings and calendar timings getters) have a optional
``params`` argument, it takes a :class:`Parameters` object and it is set to an
empty one (``Parameters()`` no arguments passed to it so it is set to its params)
by default.

It is used to adjust prayer times calculation or when prayer times is lil bit off ..etc

.. code-block:: py

    tune = aladhan.Tune(asr=20, isha=-15)
    dft = aladhan.Parameters(
        method=aladhan.methods.EGYPT,  # calculation method
        tune=tune, # to offset returned timings.
        school=aladhan.Schools.SHAFI,
        midnightMode=aladhan.MidnightModes.STANDARD,
        latitudeAdjustmentMethod=aladhan.LatitudeAdjustmentMethod.ONE_SEVENTH,
        adjustment=2
    )
    timings = await client.get_timings(latitude=34, longitude=3, params=dft)

Other Data
----------

You can also use other data that are given from the API, you can access to it
using :attr:`Timings.data` a :class:`Data` object. Look into its :class:`docs <Data>`
for more info.


Don't understand something or need some help ? join our `support server <https://discord.gg/jeBGF8Veud>`_.

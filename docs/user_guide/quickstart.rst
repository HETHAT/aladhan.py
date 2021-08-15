.. currentmodule:: aladhan

.. _quickstart:

Quickstart
==========

This page gives a brief introduction to the library. It assumes you have the
library installed, if you don’t check the :ref:`installing` portion.

Creating Client
---------------

.. note::
    If you’re new to python you don’t need to use the asynchronous client.

.. tab:: Synchronous

    .. code-block:: py

        import aladhan

        client = aladhan.Client()

    .. note::

        Although it is not required but you can close the session after done
        using the client by doing ``client.close()`` or you can use context
        manager to do it for you

        .. code:: py

            with aladhan.Client() as client:
                ...


.. tab:: Asynchronous

    .. code-block:: py

        import aladhan
        import asyncio

        async def main():
            client = aladhan.Client(is_async=True)

    .. warning::

        Don't forget to close the session after done using the client by
        doing ``await client.close()`` or you can use context manager to do
        it for you

        .. code:: py

            async with aladhan.Client(is_async=True) as client:
                ...

Of course this will do nothing but we are going to use the client soon.

.. _ref-timings:

Timings (Day Timings)
---------------------

Want to get your prayer times ? you can use :meth:`Client.get_timings`  which will return
a :class:`Timings` object:

.. tab:: Synchronous

    .. code-block:: py

        import aladhan

        client = aladhan.Client()
        timings: aladhan.Timings = client.get_timings(latitude=34, longitude=3)
        for prayer in timings:
            print(prayer.name, prayer.time)

.. tab:: Asynchronous

    .. code-block:: py

        import aladhan
        import asyncio

        async def main():
            client = aladhan.Client(is_async=True)
            timings: aladhan.Timings = await client.get_timings(latitude=34, longitude=3)
            for prayer in timings:
                print(prayer.name, prayer.time)
            await client.close()

        asyncio.run(main())

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
use :class:`TimingsDateArg`:

.. tab:: Synchronous

    .. code-block:: py

        timings: aladhan.Timings = client.get_timings(
            latitude=34,
            longitude=3,
            # TimingsDateArg takes one argument and it can
            # be a string in a DD-MM-YYYY format or
            # or a datetime.datetime obj or
            # or an int representing a unix date
            date=aladhan.TimingsDateArg("28-05-2022")
        )

.. tab:: Asynchronous

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
You can use :meth:`Client.get_timings_by_address`

.. _ref-ts-by-address:

.. tab:: Synchronous

    .. code-block:: py

        timings: aladhan.Timings = client.get_timings_by_address(address="United Kingdom, London")

.. tab:: Asynchronous

    .. code-block:: py

        timings: aladhan.Timings = await client.get_timings_by_address(address="United Kingdom, London")


or use :meth:`Client.get_timings_by_city`

.. tab:: Synchronous

    .. code-block:: py

        timings: aladhan.Timings = client.get_timings_by_city(country="United Kingdom", city="London")

.. tab:: Asynchronous

    .. code-block:: py

        timings: aladhan.Timings = await client.get_timings_by_city(country="United Kingdom", city="London")

You can configure more using :class:`Parameters`, look into :ref:`ref-conf`.

Calendar Timings
----------------
If you want to get the prayer times of more than just 1 day you
can use :meth:`Client.get_calendar` which will return a list of
:class:`Timings`.

.. tab:: Synchronous

    .. code-block:: py

        month_calendar = client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(
                year=2021,
                month=1
            )
        )

.. tab:: Asynchronous

    .. code-block:: py

        month_calendar = await client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(
                year=2021,
                month=1
            )
        )

``month`` argument for :class:`CalendarDateArg` is optional, and by not providing it
or passing 0, it will return a *year calendar*, a dict of strings ("1",...,"12")
and list of :class:`Timings` object.

.. tab:: Synchronous

    .. code-block:: py

        year_calendar = client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(year=2021)
        )

.. tab:: Asynchronous

    .. code-block:: py

        year_calendar = await client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(year=2021)
        )

you can also use *hijri* date by setting ``hijri`` argument to ``True``

.. tab:: Synchronous

    .. code-block:: py

        year_calendar = client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(year=1442, hijri=True)  # month arg still can be used
            )

.. tab:: Asynchronous

    .. code-block:: py

        year_calendar = await client.get_calendar(
            latitude=34,
            longitude=3,
            date=aladhan.CalendarDateArg(year=1442, hijri=True)  # month arg still can be used
            )

And as for using coordinates, you can use address using :meth:`Client.get_calendar_by_address`
or city/country using :meth:`Client.get_calendar_by_city`,
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
    params = aladhan.Parameters(
        method=aladhan.methods.EGYPT,  # calculation method
        tune=tune, # to offset returned timings.
        school=aladhan.Schools.SHAFI,
        midnightMode=aladhan.MidnightModes.STANDARD,
        latitudeAdjustmentMethod=aladhan.LatitudeAdjustmentMethod.ONE_SEVENTH,
        adjustment=2
    )

then you can do

.. tab:: Synchronous

    .. code-block:: py

        timings = client.get_timings(latitude=34, longitude=3, params=params)

.. tab:: Asynchronous

    .. code-block:: py

        timings = await client.get_timings(latitude=34, longitude=3, params=params)

Other Data
----------

You can also use other data that are given from the API, you can access to it
using :attr:`Timings.data` a :class:`Data` object. Look into its :class:`docs <Data>`
for more info.


Don't understand something or need some help ? join our `support server <https://discord.gg/jeBGF8Veud>`_.

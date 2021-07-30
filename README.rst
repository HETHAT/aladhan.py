``aladhan.py`` is a pythonic wrapper for the `Aladhan prayer times <https://aladhan.com/prayer-times-api>`_ API.

.. image:: https://img.shields.io/pypi/v/aladhan.py?color=blue
    :target: https://pypi.python.org/pypi/aladhan.py
    :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/aladhan.py?color=blue
    :target: https://pypi.python.org/pypi/aladhan.py
    :alt: Supported Python versions
.. image:: https://img.shields.io/discord/831992562986123376.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2
    :target: https://discord.gg/jeBGF8Veud
    :alt: Discord support server
.. image:: https://codecov.io/gh/HETHAT/aladhan.py/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/HETHAT/aladhan.py
    :alt: Code coverage

Installation
------------

**Python 3.6 or higher is required.**

To Install ``aladhan.py`` with pip:

.. code:: sh

    pip install aladhan.py

To install only with synchronous requirements

.. code:: sh

    pip install aladhan.py[sync]

To install only with asynchronous requirements

.. code:: sh

    pip install aladhan.py[async]

Quick Example
-------------

.. code:: py

    import aladhan

    client = aladhan.Client()
    prayer_times = client.get_timings_by_address("London")
    for prayer_time in prayer_times:
        print(prayer_time)

*You can look into more examples* `here <https://github.com/HETHAT/aladhan.py/tree/main/examples>`_

Contribute
----------

- `Source Code <https://github.com/HETHAT/aladhan.py>`_
- `Issue Tracker <https://github.com/HETHAT/aladhan.py/issues>`_


Support
-------

If you are having issues, please let me know by joining the `discord support server <https://discord.gg/jeBGF8Veud>`_

License
-------

The project is licensed under the MIT license.

Links
------

- `PyPi <https://pypi.python.org/pypi/aladhan.py>`_
- `Discord support server <https://discord.gg/jeBGF8Veud>`_
- `Documentation <https://aladhanpy.readthedocs.io/en/latest>`_
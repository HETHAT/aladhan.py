.. currentmodule:: aladhan

.. _api:

API Reference
=============

The following section documents every class and function in the aladhan.py module.

Version Related Info
--------------------

There are two main ways to query version information about the library.

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are
    'alpha', 'beta', 'candidate' and 'final'.

.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0rc1'``. This is based
    off of :pep:`440`.

Client
-------

.. autoclass:: Client()
    :members:
    :member-order: bysource

Timings Related
---------------

Timings
+++++++

.. autoclass:: Timings()
    :members:

Prayer
++++++

.. autoclass:: Prayer()
    :members:

Tune
++++

.. autoclass:: Tune()
    :members:

Parameters Related
------------------

Parameters
++++++++++

.. autoclass:: Parameters()
    :members:


Timings Date Argument
+++++++++++++++++++++

.. autoclass:: TimingsDateArg()
    :members:

Calendar Date Argument
++++++++++++++++++++++

.. autoclass:: CalendarDateArg()
    :members:

Calculation Methods
+++++++++++++++++++

Method
******

.. autoclass:: Method()
    :members:

Available Methods
*****************

.. csv-table::
    :header: "Method", "ID", "Name"
    :widths: 10, 3, 50

    "JAFARI", 0, "Shia Ithna-Ashari, Leva Institute, Qum"
    "KARACHI", 1, "University of Islamic Sciences, Karachi"
    "ISNA", 2, "Islamic Society of North America (ISNA)"
    "MWL", 3, "Muslim World League"
    "MAKKAH", 4, "Umm Al-Qura University Makkah"
    "EGYPT", 5, "Egyptian General Authority of Survey"
    "TEHRAN", 7, "Institute of Geophysics, University of Tehran"
    "GULF", 8, "Gulf Region"
    "KUWAIT", 9, "Kuwait"
    "QATAR", 10, "Qatar"
    "SINGAPORE", 11, "Majlis Ugama Islam Singapura, Singapore"
    "FRANCE", 12, "Union Organization Islamic de France"
    "TURKEY", 13, "Diyanet \u0130\u015fleri Ba\u015fkanl\u0131\u011f\u0131, Turkey"
    "RUSSIA", 14, "Spiritual Administration of Muslims of Russia"
    "MOONSIGHTING", 15, "Moonsighting Committee Worldwide (Moonsighting.com)"

.. note::
    - There is no 6 (method 6 is apparently same as 2).
    - Method 15 requires a shafaq parameter.

**all_methods**: dict[:class:`int`, :class:`Method`]
    A dict of each id and its method.

Data Classes
------------

Data
++++

.. autoclass:: Data()
    :members:

Meta
++++

.. autoclass:: Meta()
    :members:

Base Date
+++++++++

.. autoclass:: BaseDate()
    :members:

Date
++++

.. autoclass:: Date()
    :members:

DateType
++++++++

.. autoclass:: DateType()
    :members:


Ism
+++

.. autoclass:: Ism()
    :members:

Qibla
+++++

.. autoclass:: Qibla()
    :members:

Enums
-----

.. automodule:: aladhan.enums
    :members:
    :undoc-members:
    :member-order: bysource

.. _ref-exceptions:

Exceptions
----------

The following exceptions are thrown by the library.

.. automodule:: aladhan.exceptions
    :members:
    :member-order: bysource

Exception Hierarchy
+++++++++++++++++++

    - :exc:`Exception`
        - :exc:`~aladhan.exceptions.AladhanException`
            - :exc:`~aladhan.exceptions.HTTPException`
                - :exc:`~aladhan.exceptions.BadRequest`
                - :exc:`~aladhan.exceptions.TooManyRequests`
                - :exc:`~aladhan.exceptions.InternalServerError`
            - :exc:`~aladhan.exceptions.InvalidArgument`
                - :exc:`~aladhan.exceptions.InvalidMethod`
                - :exc:`~aladhan.exceptions.InvalidTune`
                - :exc:`~aladhan.exceptions.InvalidSchool`
                - :exc:`~aladhan.exceptions.InvalidMidnightMode`
                - :exc:`~aladhan.exceptions.InvalidTimezone`
                - :exc:`~aladhan.exceptions.InvalidLatAdjMethod`
                - :exc:`~aladhan.exceptions.InvalidAdjustment`
                - :exc:`~aladhan.exceptions.InvalidShafaq`

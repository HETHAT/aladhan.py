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
------

.. autoclass:: AsyncClient()
    :members:

Data
----

.. autoclass:: Data()
    :members:
    :undoc-members:

Timings
-------

.. autoclass:: Timings()
    :members:
    :undoc-members:

Meta
----

.. autoclass:: Meta()
    :members:
    :undoc-members:

Date
----

.. autoclass:: Date()
    :members:
    :undoc-members:

DateType
--------

.. autoclass:: DateType()
    :members:
    :undoc-members:

Prayer
------

.. autoclass:: Prayer()
    :members:
    :undoc-members:

Tune
----

.. autoclass:: Tune()
    :members:
    :undoc-members:

Ism
---

.. autoclass:: Ism()
    :members:

Qibla
-----

.. autoclass:: Qibla()
    :members:

Date Arguments
--------------

Timings Date Argument
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: TimingsDateArg()
    :members:
    :undoc-members:

Calendar Date Argument
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: CalendarDateArg()
    :members:
    :undoc-members:

Default Arguments
-----------------

.. autoclass:: DefaultArgs()
    :members:
    :undoc-members:

Enums
-----

.. automodule:: aladhan.enums_classes
    :members:
    :undoc-members:
    :member-order: bysource

Calculation Methods
-------------------

.. automodule:: aladhan.methods
    :members:
    :undoc-members:
    :member-order: bysource

Exceptions
----------

.. automodule:: aladhan.exceptions
    :members:
    :member-order: bysource

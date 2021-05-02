.. _api:

.. currentmodule:: aladhan

API Reference
=============

The following section documents every class and function in the baguette module.

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

Date Arguments
--------------

Timings Date Argument
*********************

.. autoclass:: TimingsDateArg()
    :members:
    :undoc-members:

Calendar Date Argument
**********************

.. autoclass:: CalendarDateArg()
    :members:
    :undoc-members:

Default Arguments
-----------------

.. autoclass:: DefaultArgs()
    :members:
    :undoc-members:

Latitude Adjustment Methods
---------------------------

.. autoclass:: LatitudeAdjustmentMethods()
    :members:
    :undoc-members:
    :member-order: bysource

Midnight Modes
--------------

.. autoclass:: MidnightModes()
    :members:
    :undoc-members:
    :member-order: bysource

Schools
-------

.. autoclass:: Schools()
    :members:
    :undoc-members:
    :member-order: bysource


Calculation Methods
-------------------

.. automodule:: aladhan.methods
    :members:
    :undoc-members:
    :member-order: bysource
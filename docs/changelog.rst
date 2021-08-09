.. currentmodule:: aladhan

.. _change_log:

Changelog
=========

v1.2.0 (Unreleased)
-------------------

**Added**

- Covered current event endpoints.
    - :meth:`Client.get_current_time`
    - :meth:`Client.get_current_date`
    - :meth:`Client.get_current_timestamp`
    - :meth:`Client.get_current_islamic_year`
    - :meth:`Client.get_current_islamic_month`
- Covered holidays endpoints.
    - :meth:`Client.get_next_hijri_holiday`
    - :meth:`Client.get_hijri_holidays`
    - :meth:`Client.get_islamic_holidays`
- Covered info endpoints
    - :meth:`Client.get_status`
    - :meth:`Client.get_special_days`
    - :meth:`Client.get_islamic_months`

**Changed**

- Fixed date converters, they were switched around :l

v1.1.0
------

**Added**

- Covering more 5 endpoints about date converting
    - :meth:`Client.get_hijri_from_gregorian`
    - :meth:`Client.get_gregorian_from_hijri`
    - :meth:`Client.get_hijri_calendar_from_gregorian`
    - :meth:`Client.get_gregorian_calendar_from_hijri`
    - :meth:`Client.get_islamic_year_from_gregorian_for_ramadan`

**Changed**

- The following are now optional
    - :attr:`Date.data`
    - :attr:`Date.readable`
    - :attr:`Date.timestamp`

v1.0.0
------

**Added**

- Synchronous usage for the module !
- ``__all__`` and ``__slots__`` for better performance.
- :ref:`Module exceptions <ref-exceptions>`.
- ``logging`` is now implemented.
- :meth:`Method.params_str` a string in ``"fajr,maghrib,isha"`` format.

**Changed**

- Renamed ``DefaultArgs`` to ``Parameters``
    - Renamed ``Meta.default_args`` to ``Meta.parameters``
    - Renamed ``defaults`` parameter in all getters to ``params``
- ``Timings.next_prayer`` now returns ``None`` instead if upcoming prayer wasn't in date. and Its no longer awaitable.
- :meth:`Method.params` changed to be a property
- :class:`Schools`, :class:`MidnightModes`, :class:`LatitudeAdjustmentMethods` are now enums.

**Removed**

- ``AsyncClient``. Replaced with ``Client(is_async=True)`` instead.

v0.2.0
------

**Added**

- method ``close`` for ``AsyncClient``
- custom method.
- timezone param for :class:`DefaultArgs`
- async context manager for ``AsyncClient``

**Removed**

- beartype.

v0.1.4
------

**Added**

- :attr:`Timings.as_dict`
- ``__hash__`` for the rest of base types.

**Changed**

- Renamed ``AsyncClient.__get_res`` to ``AsyncClient._get_res``
- Renamed ``AsyncClient.__get_timings`` to ``AsyncClient._get_timings``

v0.1.3
------

**Added**

- :meth:`AsyncClient.get_qibla`
- :meth:`AsyncClient.get_asma`
- :meth:`AsyncClient.get_all_asma`
- :class:`Qibla`
- :class:`Ism`

v0.1.2
------

**Added**

- :attr:`Prayer.time_utc` Prayer time in utc.
- :attr:`Prayer.remaining_utc` Remaining time for prayer for utc.
- :attr:`Prayer.timings` Original :class:`Timings` obj.

**Changed**

- Fixed :exc:`RuntimeError` Saying event loop is closed.

**Removed**

- Removed Caching
- Removed ``AsyncClient.close``

v0.1.1
------

- Fix :attr:`Timings.next_prayer` bug when next prayer is going to be fajr.

v0.1.0
------

**Added**

- forgotten requirement.
- ``__hash__`` to some classes.

**Changed**

- :class:`AsyncClient` getters no longer return :class:`Data` object the return now :class:`Timings` instead, you can still get the :class:`Data` object using :attr:`Timings.data`.
- Edited docsstrings to make it more readable.
- Edited examples so they work for the new release.

**Removed**

- all ``__str__`` methods and replaced it with ``__repr__``.

v0.0.2
------

- Added examples.
- Fixed imports.

v0.0.1
------

- Test release.

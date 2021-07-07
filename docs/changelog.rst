.. currentmodule:: aladhan

Changelog
=========

v0.2.0
------

- Add method ``close`` for ``AsyncClient``
- Add custom method.
- Add timezone param for :class:`DefaultArgs`
- Add async context manager for ``AsyncClient``
- Remove beartype.

v0.1.4
------

- Add :attr:`Timings.as_dict`
- Add ``__hash__`` for the rest of base types.
- Rename ``AsyncClient.__get_res`` to ``AsyncClient._get_res``
- Rename ``AsyncClient.__get_timings`` to ``AsyncClient._get_timings``

v0.1.3
------

- Add :meth:`AsyncClient.get_qibla`
- Add :meth:`AsyncClient.get_asma`
- Add :meth:`AsyncClient.get_all_asma`
- Add :class:`Qibla`
- Add :class:`Ism`

v0.1.2
------

- Add :attr:`Prayer.time_utc` Prayer time in utc.
- Add :attr:`Prayer.remaining_utc` Remaining time for prayer for utc.
- Add :attr:`Prayer.timings` Original :class:`Timings` obj.
- Remove Caching
- Remove ``AsyncClient.close``
- Fix :exc:`RuntimeError` Saying event loop is closed.

v0.1.1
------

- Fix :attr:`Timings.next_prayer` bug when next prayer is going to be fajr.

v0.1.0
------

- :class:`AsyncClient` getters no longer return :class:`Data` object the return now :class:`Timings` instead, you can still get the :class:`Data` object using :attr:`Timings.data`.
- Edi docsstrings to make it more readable.
- Remove all ``__str__`` methods and replaced it with ``__repr__``.
- implement ``__hash__`` to some classes.
- Add a forgotten requirement.
- Edit examples so they work for the new release.

v0.0.2
------

- Add examples.
- Fix imports.

v0.0.1
------

- Test release.

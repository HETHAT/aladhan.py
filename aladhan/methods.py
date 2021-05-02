"""
JAFARI: :class:`Method`
    0, Shia Ithna-Ashari, Leva Institute, Qum

KARACHI: :class:`Method`
    1, University of Islamic Sciences, Karachi

ISNA: :class:`Method`
    2, Islamic Society of North America (ISNA)

MWL: :class:`Method`
    3, Muslim World League

MAKKAH: :class:`Method`
    4, Umm Al-Qura University Makkah

EGYPT: :class:`Method`
    5, Egyptian General Authority of Survey

.. note::
    There is no 6 (method 6 is apparently same as 2).

TEHRAN: :class:`Method`
    7, Institute of Geophysics, University of Tehran

GULF: :class:`Method`
    8, Gulf Region

KUWAIT: :class:`Method`
    9, Kuwait

QATAR: :class:`Method`
    10, Qatar

SINGAPORE: :class:`Method`
    11, Majlis Ugama Islam Singapura, Singapore

FRANCE: :class:`Method`
    12, Union Organization Islamic de France

TURKEY: :class:`Method`
    13, Diyanet \u0130\u015fleri Ba\u015fkanl\u0131\u011f\u0131, Turkey

RUSSIA: :class:`Method`
    14, Spiritual Administration of Muslims of Russia

MOONSIGHTING: :class:`Method`
    15, Moonsighting Committee Worldwide (Moonsighting.com)

all_methods: dict[:class:`int`, :class:`Method`]
    A dict of each id and its method.
"""


class Method:
    """
    Represents a Method Calculation obj.

    Attributes
    ----------
        name: :class:`str`
            Method name.

        id: :class:`int`
            Method id that will be used to get response.
            Can be only from 0 to 15.

        params: :class:`dict`
            Method params.
    """

    def __init__(self, name: str, id: int, params: dict):
        self.name = name
        self.id = id
        self.params = params

    def __repr__(self):  # pragma: no cover
        return "<Method name={0.name!r}, id={0.id}>".format(self)

    def __hash__(self):  # pragma: no cover
        return hash((self.name, self.id))


JAFARI = Method(
    name="Shia Ithna-Ashari, Leva Institute, Qum",
    id=0,
    params={"Fajr": 16, "Isha": 14, "Maghrib": 4, "Midnight": "JAFARI"},
)
KARACHI = Method(
    name="University of Islamic Sciences, Karachi",
    id=1,
    params={"Fajr": 18, "Isha": 18},
)
ISNA = Method(
    name="Islamic Society of North America (ISNA)",
    id=2,
    params={"Fajr": 15, "Isha": 15},
)
MWL = Method(name="Muslim World League", id=3, params={"Fajr": 18, "Isha": 17})
MAKKAH = Method(
    name="Umm Al-Qura University, Makkah",
    id=4,
    params={"Fajr": 18.5, "Isha": "90 min"},
)
EGYPT = Method(
    name="Egyptian General Authority of Survey",
    id=5,
    params={"Fajr": 19.5, "Isha": 17.5},
)
# there is no 6 (method 6 is apparently same as 2)
TEHRAN = Method(
    name="Institute of Geophysics, University of Tehran",
    id=7,
    params={"Fajr": 17.7, "Isha": 14, "Maghrib": 4.5, "Midnight": "JAFARI"},
)
GULF = Method(name="Gulf Region", id=8, params={"Fajr": 19.5, "Isha": "90 min"})
KUWAIT = Method(name="Kuwait", id=9, params={"Fajr": 18, "Isha": 17.5})
QATAR = Method(name="Qatar", id=10, params={"Fajr": 18, "Isha": "90 min"})
SINGAPORE = Method(
    name="Majlis Ugama Islam Singapura, Singapore",
    id=11,
    params={"Fajr": 20, "Isha": 18},
)
FRANCE = Method(
    name="Union Organization Islamic de France",
    id=12,
    params={"Fajr": 12, "Isha": 12},
)
TURKEY = Method(
    name="Diyanet \u0130\u015fleri Ba\u015fkanl\u0131\u011f\u0131, Turkey",
    id=13,
    params={"Fajr": 18, "Isha": 17},
)
RUSSIA = Method(
    name="Spiritual Administration of Muslims of Russia",
    id=14,
    params={"Fajr": 16, "Isha": 15},
)
MOONSIGHTING = Method(
    name="Moonsighting Committee Worldwide (Moonsighting.com)",
    id=15,
    params={"shafaq": "general"},
)
# CUSTOM = Method(
#     name="Custom",
#     id=99,
#     params={}
# )
# later

all_methods = {
    0: JAFARI,
    1: KARACHI,
    2: ISNA,
    3: MWL,
    4: MAKKAH,
    5: EGYPT,
    # rip 6
    7: TEHRAN,
    8: GULF,
    9: KUWAIT,
    10: QATAR,
    11: SINGAPORE,
    12: FRANCE,
    13: TURKEY,
    14: RUSSIA,
    15: MOONSIGHTING,
    # 99 later
}

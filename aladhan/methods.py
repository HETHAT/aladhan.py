__all__ = (
    "Method",
    "JAFARI",
    "KARACHI",
    "ISNA",
    "MWL",
    "MAKKAH",
    "EGYPT",
    "TEHRAN",
    "GULF",
    "KUWAIT",
    "QATAR",
    "SINGAPORE",
    "FRANCE",
    "TURKEY",
    "RUSSIA",
    "MOONSIGHTING",
    "all_methods",
)


class Method:
    """
    Represents a Method Calculation obj. Can be used to create a Custom Method.
    To make a custom method:

    .. code:: py

        params = {
            "fajr": ...,  # can be either an `int` or "null", \
                if it was not giving it will be set to "null".
            "maghrib": ...,
            "isha": ...
        }
        # id must be 99. Name param doesn't effect.
        custom_method = Method("Custom", 99, params=params)

    Attributes
    ----------
        name: :class:`str`
            Method name.

        id: :class:`int`
            Method id that will be used to get response.
            Can be only from 0 to 15.
    """

    __slots__ = ("name", "id", "__params", "__params_str")

    def __init__(self, name: str, id: int, params: dict):
        self.name = name
        self.id = id
        self.__params = params
        lst = []
        for t in ("fajr", "magrib", "isha"):
            v = params.get(t, "null")
            if not isinstance(v, int) and v != "null":
                raise TypeError(
                    (
                        "params '{}' expected to be type of `int` or "
                        '"null", got `{}`'
                    ).format(t, type(v).__name__)
                )
            lst.append(str(v))
        self.__params_str = ",".join(lst)

    @property
    def params(self):
        """
        Method parameters.

        *Changed in v1.0.0 to a property.*
        """
        return self.__params

    @property
    def params_str(self):
        """
        A string in "fajr,maghrib,isha" format.

        *New in v1.0.0*
        """
        return self.__params_str

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
GULF = Method(
    name="Gulf Region", id=8, params={"Fajr": 19.5, "Isha": "90 min"}
)
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
}

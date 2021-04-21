
class Method:
    def __init__(self, name: str, id: int, params: dict):
        self.name = name
        self.id = id
        self.params = params

    def __str__(self):
        return "<Method name={0.name!r}, id={0.id}, params={0.params}>".format(self)

    def __repr__(self):
        return "<Method object>"


JAFARI = Method(
    "Shia Ithna-Ashari, Leva Institute, Qum",
    0,
    {"Fajr": 16, "Isha": 14, "Maghrib": 4, "Midnight": "JAFARI"},
)
KARACHI = Method("University of Islamic Sciences, Karachi", 1, {"Fajr": 18, "Isha": 18})
ISNA = Method("Islamic Society of North America (ISNA)", 2, {"Fajr": 15, "Isha": 15})
MWL = Method("Muslim World League", 3, {"Fajr": 18, "Isha": 17})
MAKKAH = Method("Umm Al-Qura University, Makkah", 4, {"Fajr": 18.5, "Isha": "90 min"})
EGYPT = Method("Egyptian General Authority of Survey", 5, {"Fajr": 19.5, "Isha": 17.5})
# there is no 6 (method 6 is apparently same as 2)
TEHRAN = Method(
    "Institute of Geophysics, University of Tehran",
    7,
    {"Fajr": 17.7, "Isha": 14, "Maghrib": 4.5, "Midnight": "JAFARI"},
)
GULF = Method("Gulf Region", 8, {"Fajr": 19.5, "Isha": "90 min"})
KUWAIT = Method("Kuwait", 9, {"Fajr": 18, "Isha": 17.5})
QATAR = Method("Qatar", 10, {"Fajr": 18, "Isha": "90 min"})
SINGAPORE = Method(
    "Majlis Ugama Islam Singapura, Singapore", 11, {"Fajr": 20, "Isha": 18}
)
FRANCE = Method("Union Organization Islamic de France", 12, {"Fajr": 12, "Isha": 12})
TURKEY = Method(
    "Diyanet \u0130\u015fleri Ba\u015fkanl\u0131\u011f\u0131, Turkey",
    13,
    {"Fajr": 18, "Isha": 17},
)
RUSSIA = Method(
    "Spiritual Administration of Muslims of Russia",
    14,
    {"Fajr": 16, "Isha": 15},
)
MOONSIGHTING = Method(
    "Moonsighting Committee Worldwide (Moonsighting.com)",
    15,
    {"shafaq": "general"},
)
# CUSTOM = Method(
#     "Custom",
#     99,
#     {}
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

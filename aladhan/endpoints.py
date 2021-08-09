BASE = "https://api.aladhan.com/v1/"

# Next Prayer
NEXT_PRAYER_BY_ADDRESS = BASE + "nextPrayerByAddress"  # todo
# ...

# Timings
TIMINGS = BASE + "timings"
TIMINGS_BY_ADDRESS = TIMINGS + "ByAddress"
TIMINGS_BY_CITY = TIMINGS + "ByCity"

# Calendar
CALENDAR = BASE + "calendar"
CALENDAR_BY_ADDRESS = CALENDAR + "ByAddress"
CALENDAR_BY_CITY = CALENDAR + "ByCity"

# Hijri Calendar
HIJRI_CALENDAR = BASE + "hijriCalendar"
HIJRI_CALENDAR_BY_ADDRESS = HIJRI_CALENDAR + "ByAddress"
HIJRI_CALENDAR_BY_CITY = HIJRI_CALENDAR + "ByCity"

# Info
STATUS = BASE + "status"
METHODS = BASE + "methods"  # won't be covered (use aladhan.methods instead)
SPECIAL_DAYS = BASE + "specialDays"
ISLAMIC_MONTHS = BASE + "islamicMonths"

# Date Converters
H_TO_G = BASE + "hToG"
G_TO_H = BASE + "gToH"
G_TO_H_CALENDAR = BASE + "gToHCalendar/%d/%d?adjustment=%d"
H_TO_G_CALENDAR = BASE + "hToGCalendar/%d/%d?adjustment=%d"
ISLAMIC_YEAR_FROM_G_FOR_RAMADAN = (
    BASE + "islamicYearFromGregorianForRamadan/%d"
)

# Holidays
NEXT_HIJRI_HOLIDAY = BASE + "nextHijriHoliday"
HIJRI_HOLIDAYS = BASE + "hijriHolidays/%d/%d"
ISLAMIC_HOLIDAYS_BY_H_YEAR = (
    BASE + "islamicHolidaysByHijriYear/%d?adjustment=%d"
)

# Current ...
CURRENT_TIME = BASE + "currentTime"
CURRENT_DATE = BASE + "currentDate"
CURRENT_TIMESTAMP = BASE + "currentTimestamp"
CURRENT_ISLAMIC_YEAR = BASE + "currentIslamicYear"
CURRENT_ISLAMIC_MONTH = BASE + "currentIslamicMonth"

# Others
ASMA_AL_HUSNA = BASE + "asmaAlHusna/%s"
QIBLA = BASE + "qibla/%f/%f"

from hijriconverter import calendars
from datetime import date
import bisect


class Hijri:
    """A Hijri object represents a date (year, month and day) in Hijri
    calendar.
    """

    def __new__(cls, year: int, month: int, day: int) -> "Hijri":
        """Construct Hijri date object after date validation"""
        _check_hijri_date(year, month, day)
        return super().__new__(cls)

    def __init__(self, year: int, month: int, day: int) -> None:
        """
        :param year: Hijri year
        :type year: int
        :param month: Hijri month
        :type month: int
        :param day: Hijri day
        :type day: int
        """

        self._year = year
        self._month = month
        self._day = day

    def __repr__(self) -> str:
        return f"Hijri({self._year}, {self._month}, {self._day})"

    def __str__(self) -> str:
        return self.isoformat()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hijri):
            raise TypeError("second operand must be 'Hijri' object")
        return self.datetuple() == other.datetuple()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Hijri):
            raise TypeError("second operand must be 'Hijri' object")
        return self.datetuple() > other.datetuple()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Hijri):
            raise TypeError("second operand must be 'Hijri' object")
        return self.datetuple() >= other.datetuple()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Hijri):
            raise TypeError("second operand must be 'Hijri' object")
        return self.datetuple() < other.datetuple()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Hijri):
            raise TypeError("second operand must be 'Hijri' object")
        return self.datetuple() <= other.datetuple()

    @classmethod
    def fromisoformat(cls, date_string: str):
        """Construct Hijri object from an ISO formatted Hijri date
        'YYYY-MM-DD'.

        :param date_string: Hijri date in ISO format ``YYYY-MM-DD``
        :type date_string: str

        """

        year = int(date_string[0:4])
        month = int(date_string[5:7])
        day = int(date_string[8:10])
        return cls(year, month, day)

    @property
    def year(self) -> int:
        """Return Hijri year as an integer."""
        return self._year

    @property
    def month(self) -> int:
        """Return Hijri month as an integer."""
        return self._month

    @property
    def day(self) -> int:
        """Return Hijri day as an integer."""
        return self._day

    def datetuple(self) -> tuple:
        """Return Hijri date as a tuple of (year, month, day)."""
        return self._year, self._month, self._day

    def isoformat(self) -> str:
        """Return Hijri date in ISO format 'YYYY-MM-DD'."""
        return f"{self._year:04}-{self._month:02}-{self._day:02}"

    def slashformat(self) -> str:
        """Return Hijri date in slash format 'DD/MM/YYYY'."""
        return f"{self._day:02}/{self._month:02}/{self._year:04}"

    def month_length(self) -> int:
        """Return number of days in Hijri month."""
        month_index = _hijri_month_index(self._year, self._month)
        month_length = _hijri_month_length(month_index)
        return month_length

    def month_name(self, language: str = "en") -> str:
        """Return Hijri month name.

        :param language: language which may be ``en`` or ``ar``
            (default is ``en``)
        :type language: str
        """

        return calendars.Hijri.month_names[language][self._month]

    def weekday(self) -> int:
        """Return day of week, where Monday is 0 ... Sunday is 6."""
        jd = self.to_julian()
        return int(jd % 7)

    def isoweekday(self) -> int:
        """Return day of week, where Monday is 1 ... Sunday is 7."""
        jd = self.to_julian()
        return int(jd % 7) + 1

    def day_name(self, language: str = "en") -> str:
        """Return day name.

        :param language: language which may be ``en`` or ``ar``
            (default is ``en``)
        :type language: str
        """

        return calendars.day_names[language][self.weekday()]

    @staticmethod
    def notation(language: str = "en") -> str:
        """Return calendar notation/abbreviation.

        :param language: language which may be ``en`` or ``ar``
            (default is ``en``)
        :type language: str
        """

        return calendars.Hijri.notations[language]

    def to_julian(self) -> int:
        """Convert Hijri date to Julian day number."""
        month_starts = calendars.Hijri.month_starts
        index = _hijri_month_index(self._year, self._month)
        rjd = self._day + month_starts[index - 1] - 1
        jd = _reduced_julian_to_julian(rjd)
        return jd

    def to_gregorian(self) -> "Gregorian":
        """Convert Hijri date to Gregorian date.

        :return: Gregorian date object
        :rtype: Gregorian
        """

        jd = self.to_julian()
        rd = _julian_to_ordinal(jd)
        return Gregorian.fromordinal(rd)


class Gregorian(date):
    """A Gregorian object represents a date (year, month and day) in Gregorian
    calendar inheriting all attributes and methods of `datetime.date` object.
    """

    @classmethod
    def fromdate(cls, date_object: date) -> "Gregorian":
        """Construct Gregorian object from a date object.

        :param date_object: Date object
        :type date_object: datetime.date
        """

        year, month, day = date_object.timetuple()[:3]
        return cls(year, month, day)

    def datetuple(self) -> tuple:
        """Return Gregorian date as a tuple of (year, month, day)."""
        return self.year, self.month, self.day

    def month_name(self, language: str = "en") -> str:
        """Return Hijri month name.

        :param language: language which may be ``en`` or ``ar``
            (default is ``en``)
        :type language: str
        """

        return calendars.Gregorian.month_names[language][self.month]

    def day_name(self, language: str = "en") -> str:
        """Return day name.

        :param language: language which may be ``en`` or ``ar``
            (default is ``en``)
        :type language: str
        """

        return calendars.day_names[language][self.weekday()]

    @staticmethod
    def notation(language: str = "en") -> str:
        """Return calendar notation/abbreviation.

        :param language: language which may be ``en`` or ``ar``
            (default is ``en``)
        :type language: str
        """

        return calendars.Gregorian.notations[language]

    def to_julian(self) -> int:
        """Convert Gregorian date to Julian day number."""
        jd = _ordinal_to_julian(self.toordinal())
        return jd

    def to_hijri(self) -> Hijri:
        """Convert Gregorian date to Hijri date.

        :return: Hijri date object
        :rtype: Hijri
        """

        _check_gregorian_range(*self.datetuple())
        jd = self.to_julian()
        rjd = _julian_to_reduced_julian(jd)
        month_starts = calendars.Hijri.month_starts
        index = bisect.bisect_right(month_starts, rjd)
        months = index + calendars.Hijri.first_offset
        years = int((months - 1) / 12)
        year = years + 1
        month = months - 12 * years
        day = rjd - month_starts[index - 1] + 1
        return _ValidHijri(year, month, day)


class _ValidHijri(Hijri):
    """A Hijri object converted from Gregorian date. This implementation is
    to avoid double checking of date.
    """

    def __new__(cls, *args, **kwargs) -> "Hijri":
        return super(Hijri, cls).__new__(cls)


def _check_gregorian_range(year: int, month: int, day: int) -> None:
    """Check if Gregorian date is within valid conversion range."""
    # check range
    valid_range = calendars.Gregorian.valid_range
    if not valid_range[0] <= (year, month, day) <= valid_range[1]:
        raise OverflowError("date is out of range for conversion")


def _check_hijri_date(year: int, month: int, day: int) -> None:
    """Check Hijri date values and if date is within valid conversion range."""
    # check year
    if len(str(year)) != 4:
        raise ValueError("year must be in yyyy format")
    # check month
    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12")
    # check range (placed in this order intentionally)
    valid_range = calendars.Hijri.valid_range
    if not valid_range[0] <= (year, month, day) <= valid_range[1]:
        raise OverflowError("date is out of range for conversion")
    # check day (if not within valid range, day could not be checked)
    month_index = _hijri_month_index(year, month)
    month_length = _hijri_month_length(month_index)
    if not 1 <= day <= month_length:
        raise ValueError(f"day must be in 1..{month_length} for month")


def _hijri_month_index(year: int, month: int) -> int:
    """Return index of month in Hijri month starts."""
    months = ((year - 1) * 12) + month
    index = months - calendars.Hijri.first_offset
    return index


def _hijri_month_length(index: int) -> int:
    """Return number of days in Hijri month."""
    month_starts = calendars.Hijri.month_starts
    length = month_starts[index] - month_starts[index - 1]
    return length


def _julian_to_ordinal(jd: int) -> int:
    """Convert Julian day number to ordinal number."""
    return jd - 1721425


def _ordinal_to_julian(rd: int) -> int:
    """Convert ordinal number to Julian day number."""
    return rd + 1721425


def _julian_to_reduced_julian(jd: int) -> int:
    """Convert Julian day number to reduced Julian day number."""
    return jd - 2400000


def _reduced_julian_to_julian(rjd: int) -> int:
    """Convert reduced Julian day number to Julian day number."""
    return rjd + 2400000

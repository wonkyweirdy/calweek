import calendar
from datetime import date, timedelta
from collections import namedtuple

__version__ = (0, 5, 0)


import sys
if sys.version_info >= (3,):
    # compatibility tweaks
    basestring = str
    long = int

class CalWeek(namedtuple('CalWeek', ('year', 'week'))):
    """A CalWeek represents a week starting with a Sunday.
    Weeks are identified by a year and week number within the year.
    This corresponds to the read-only attributes 'year' and 'week'.

    CalWeek objects are tuples, and thus immutable, with an interface
    similar to the standard datetime.date class.
    """
    __slots__ = ()

    min = None  # type: CalWeek
    max = None  # type: CalWeek
    resolution = timedelta(weeks=1)  # type: timedelta
    first_dow = 6

    def __new__(cls, year, week):
        """Initialize a CalWeek tuple with the given year and week number.

        The week must be within the range 1 to 54. The year must be within
        the range 1 to 9999.
        """
        if week < 1 or (week > 53 and week > cls.last_week_number_of_year(year)):
            raise ValueError("week is out of range")
        if year < 1 or year > 9999:
            raise ValueError("year is out of range")
        # noinspection PyArgumentList
        return super(CalWeek, cls).__new__(cls, year, week)

    @classmethod
    def thisweek(cls):
        """Return the current week (local time)."""
        return cls.withdate(date.today())

    @classmethod
    def fromordinal(cls, ordinal):
        """Return the week corresponding to the proleptic Gregorian ordinal,
        where January 1 of year 1 starts the week with ordinal 1.
        """
        if ordinal < 1:
            raise ValueError("ordinal must be >= 1")
        return cls.withdate(date.fromordinal((ordinal - 1) * 7 + 1))

    @classmethod
    def fromstring(cls, isostring):
        """Return a week initialized from an formatted string like "2011W08" or "2011-W08"."""
        if isinstance(isostring, basestring) and len(isostring) == 7 and isostring[4] == 'W':
           return cls(int(isostring[0:4]), int(isostring[5:7]))
        elif isinstance(isostring, basestring) and len(isostring) == 8 and isostring[4:6] == '-W':
           return cls(int(isostring[0:4]), int(isostring[6:8]))
        else:
            raise ValueError("CalWeek.tostring argument must be on the form <yyyy>W<ww>; got %r" % (isostring,))

    @classmethod
    def withdate(cls, date):
        """Return the week that contains the given datetime.date"""
        return cls(date.year, _weeknum(date, cls.first_dow))

    @classmethod
    def weeks_of_year(cls, year):
        """Return an iterator over the weeks of the given year.
        Years have either 52 or 53 weeks."""
        w = cls(year, 1)
        while w.year == year:
            yield w
            w += 1

    @classmethod
    def last_week_of_year(cls, year):
        """Return the last week of the given year.

        The first week of a given year is simply CalWeek(year, 1), so there
        is no dedicated classmethod for that.
        """
        return cls(year, cls.last_week_number_of_year(year))

    @classmethod
    def last_week_number_of_year(cls, year):
        year_days = 365 if calendar.isleap(year) else 364
        return (year_days - cls.days_in_first_week(year)) // 7 + 2

    @classmethod
    def days_in_first_week(cls, year):
        dt = date(year, 1, 1)
        return 7 - (dt.weekday() - cls.first_dow) % 7

    def day(self, num):  # type: (int) -> date
        """Return the nth day of week as a date object.  Day 0 is the first day."""
        num_first_week_days = self.days_in_first_week(self.year)
        dt = date(self.year, 1, 1)
        if self.week == 1:
            if num >= num_first_week_days:
                raise NonexistentDayOfWeek("No such day in this week")
            return dt + timedelta(days=num)
        result = dt + timedelta(weeks=self.week - 2, days=num_first_week_days + num)
        if result.year != self.year:
            raise NonexistentDayOfWeek("No such day in this week")
        return result

    def dow(self, num):
        """Return the given day of week as a date object.  Day 0 is Monday."""
        if self.week > 1:
            return self.day((num - self.first_dow) % 7)
        first_day_of_year = date(self.year, 1, 1)
        n = (num - first_day_of_year.weekday()) % 7
        if n >= self.days_in_first_week(self.year):
            raise NonexistentDayOfWeek("No such day in this week")
        return self.day(n)

    def monday(self):
        """Return the Monday of the week as a date object"""
        return self.dow(0)

    def tuesday(self):
        """Return the Tuesday of the week as a date object"""
        return self.dow(1)

    def wednesday(self):
        """Return the Wednesday of the week as a date object"""
        return self.dow(2)

    def thursday(self):
        """Return the Thursday of the week as a date object"""
        return self.dow(3)

    def friday(self):
        """Return the Friday of the week as a date object"""
        return self.dow(4)

    def saturday(self):
        """Return the Saturday of the week as a date object"""
        return self.dow(5)

    def sunday(self):
        """Return the Sunday of the week as a date object"""
        return self.dow(6)

    def last_day(self):
        """Return the last day of the week as a date object"""
        return self.day(self.day_count() - 1)

    def day_count(self):
        """Return the number of days in this week."""
        if self.week == 1:
            return self.days_in_first_week(self.year)
        last_week = self.last_week_of_year(self.year)
        if self.week == last_week.week:
            return 32 - last_week.day(0).day
        return 7

    def days(self):
        """Return the 7 days of the week as a list (of datetime.date objects)"""
        first_day = self.day(0)
        return [first_day + timedelta(days=i) for i in range(self.day_count())]

    def contains(self, day):
        """Check if the given datetime.date falls within the week"""
        return self.day(0) <= day <= self.day(self.day_count() - 1)

    def toordinal(self):
        """Return the proleptic Gregorian ordinal of the week, where January 1 of year 1 starts the first week."""
        return self.day(0).toordinal() // 7 + 1

    def replace(self, year=None, week=None):
        """Return a CalWeek with either the year or week attribute value replaced"""
        return self.__class__(self.year if year is None else year,
                              self.week if week is None else week)

    def year_week(self):
        """Return a regular tuple containing the (year, week)"""
        return self.year, self.week

    def __str__(self):
        """Return a formatted week string like "2011W08". """
        return '%04dW%02d' % self

    def __repr__(self):
        """Return a string like "calweek.CalWeek(2011, 35)"."""
        return __name__ + '.' + self.__class__.__name__ + '(%d, %d)' % self

    def __add__(self, other):
        """Adding integers to a CalWeek gives the week that many number of weeks into the future.
        Adding with datetime.timedelta is also supported.
        """
        if isinstance(other, timedelta):
            other = other.days // 7
        return self.__class__.fromordinal(self.toordinal() + other)

    def __sub__(self, other):
        """Subtracting two weeks give the number of weeks between them as an integer.
        Subtracting an integer gives another CalWeek in the past."""
        if isinstance(other, (int, long, timedelta)):
            return self.__add__(-other)
        return self.toordinal() - other.toordinal()

CalWeek.min = CalWeek(1, 1)
CalWeek.max = CalWeek(9999, 53)

def _weeknum(dt, first_dow):
    first_of_year = dt.replace(month=1, day=1)
    year_day = (dt - first_of_year).days
    week = (year_day + (first_of_year.weekday() + 7 - first_dow) % 7) // 7 + 1
    return week

_weeknum_first_dow_map = {1: 6, 2: 0, 11: 0, 12: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6}

def weeknum(dt, return_type=1):
    """Return a week number for the given datetime.date like Excel's WEEKNUM function"""
    if return_type == 21:
        from isoweek import Week
        return Week.withdate(dt).week
    first_dow = _weeknum_first_dow_map[return_type]
    return _weeknum(dt, first_dow)

class NonexistentDayOfWeek(ValueError):
    pass

import holidays
import datetime


class NorwegianCalendar:
    """
    Enhanced Norwegian calendar with both official holidays
    and common vacation periods
    """

    def __init__(self, year=None):
        # Get the current year if not specified
        if year is None:
            year = datetime.datetime.now().year

        # Initialize official Norwegian holidays
        self.official_holidays = holidays.Norway(years=year)

        # Initialize vacation periods
        self.vacation_periods = self._get_vacation_periods(year)

    def _get_vacation_periods(self, year):
        """Define common Norwegian vacation periods"""
        periods = {}

        # Eksamensperiode (Exam Period) - all of May plus first week of June
        # May (entire month)
        for day in range(1, 32):  # All of May
            date = datetime.date(year, 5, day)
            periods[date] = "Eksamensperiode (Exam Period)"

        # First week of June (days 1-7)
        for day in range(1, 8):
            date = datetime.date(year, 6, day)
            periods[date] = "Eksamensperiode (Exam Period)"

        # Studentferie (Student Summer Vacation) - rest of June
        for day in range(8, 31):  # June 8-30
            date = datetime.date(year, 6, day)
            periods[date] = "Studentferie (Student Summer Vacation)"

        # Fellesferie (Summer vacation) - all of July
        for day in range(1, 32):  # All of July
            date = datetime.date(year, 7, day)
            periods[date] = "Fellesferie (Summer Vacation)"

        # Studentferie (Student Summer Vacation) - first two weeks of August
        for day in range(1, 15):  # August 1-14
            date = datetime.date(year, 8, day)
            periods[date] = "Studentferie (Student Summer Vacation)"

        # Christmas break (typically Dec 20-Jan 2)
        for day in range(20, 32):  # Dec 20-31
            date = datetime.date(year, 12, day)
            if date not in self.official_holidays:  # Don't duplicate official holidays
                periods[date] = "Juleferie (Christmas Break)"

        # Add early January of the same year (continuation of Christmas break)
        for day in range(1, 3):  # Jan 1-2
            date = datetime.date(year, 1, day)
            if date not in self.official_holidays:  # Don't duplicate official holidays
                periods[date] = "Juleferie (Christmas Break)"

        # Winter break (typically week 8 or 9, varies by region)
        # This is an approximation - exact dates vary by municipality
        winter_break_start = self._get_date_of_week(year, 8, 0)  # Monday of week 8
        for i in range(7):  # Full week
            date = winter_break_start + datetime.timedelta(days=i)
            periods[date] = "Vinterferie (Winter Break)"

        # Easter break (week before and after Easter)
        # Get Easter Sunday from the holidays library
        easter_dates = [
            date
            for date, name in self.official_holidays.items()
            if name == "Første påskedag"
        ]
        if easter_dates:
            easter_sunday = easter_dates[0]
            # Week before Easter (excluding official holidays)
            for i in range(1, 7):
                date = easter_sunday - datetime.timedelta(days=i)
                if date not in self.official_holidays:
                    periods[date] = "Påskeferie (Easter Break)"

            # Week after Easter (excluding official holidays)
            for i in range(1, 7):
                date = easter_sunday + datetime.timedelta(days=i)
                if date not in self.official_holidays:
                    periods[date] = "Påskeferie (Easter Break)"

        return periods

    def _get_date_of_week(self, year, week_number, weekday):
        """Get the date of a specific weekday (0=Monday) in a specific week of the year"""
        # Create a date object for January 1st of the given year
        first_day = datetime.date(year, 1, 1)

        # Calculate the offset to the first day of week 1
        # According to ISO, week 1 is the week containing the first Thursday of the year
        first_monday = first_day + datetime.timedelta(
            days=(8 - first_day.isoweekday()) % 7
        )

        # Calculate the Monday of the desired week
        target_date = first_monday + datetime.timedelta(weeks=week_number - 1)

        # Add weekday offset
        target_date += datetime.timedelta(days=weekday)

        return target_date

    def is_special_date(self, date):
        """
        Check if a date is either an official holiday or in a vacation period

        Returns:
            tuple: (is_special, type, name)
                is_special: True if holiday or vacation period
                type: 'holiday' or 'vacation'
                name: Name of the holiday or vacation period
        """
        # Check if it's an official holiday
        if date in self.official_holidays:
            return (True, "holiday", self.official_holidays[date])

        # Check if it's in a vacation period
        if date in self.vacation_periods:
            return (True, "vacation", self.vacation_periods[date])

        # Regular day
        return (False, "regular", None)

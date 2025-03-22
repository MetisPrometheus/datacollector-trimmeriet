import os
import datetime
import csv
import logging
import pytz
from enhanced_vacation_periods import NorwegianCalendar

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, data_dir="data", csv_file="visitor_counts.csv"):
        self.data_dir = data_dir
        self.csv_path = os.path.join(data_dir, csv_file)
        self.calendar = NorwegianCalendar()  # Initialize Norwegian calendar
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Create the data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)

        # Create CSV with headers if it doesn't exist
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="\n") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "timestamp",
                        "visitor_count",
                        "temperature",
                        "weather_category",
                        "is_raining",
                        "is_daytime",
                        "is_holiday",
                        "is_vacation_period",
                        "special_date_name",
                    ]
                )

    def _round_to_15min_interval(self, dt):
        """Round timestamp to nearest 15-minute interval"""
        # Calculate minutes to nearest 15 min
        minute = dt.minute

        # Round to nearest 15 min
        if minute < 8:
            rounded_minute = 0
        elif minute < 23:
            rounded_minute = 15
        elif minute < 38:
            rounded_minute = 30
        else:
            rounded_minute = 45

        # Create new datetime with rounded minutes and zeroed seconds
        return dt.replace(minute=rounded_minute, second=0, microsecond=0)

    def _check_special_date(self, dt):
        """Check if given date is a holiday or common vacation period in Norway"""
        date_only = dt.date()
        is_special, special_type, special_name = self.calendar.is_special_date(
            date_only
        )

        is_holiday = "yes" if special_type == "holiday" else "no"
        is_vacation = "yes" if special_type == "vacation" else "no"

        if is_special:
            print(f"Today is a special date: {special_name} ({special_type})")

        return is_holiday, is_vacation, special_name

    def store_data(self, visitor_count, weather_data=None):
        """Store visitor count and weather data with timestamp on exact 15 min interval"""
        # Use local timezone (Norway)
        norway_tz = pytz.timezone("Europe/Oslo")
        now = datetime.datetime.now(norway_tz)

        # Round to nearest 15-minute interval
        rounded_time = self._round_to_15min_interval(now)
        timestamp = rounded_time.strftime("%Y-%m-%d %H:%M:%S")

        # Check if the date is a holiday or vacation period in Norway
        is_holiday, is_vacation, special_name = self._check_special_date(rounded_time)
        special_name = special_name if special_name else ""

        # Proper formatting for logging
        print(f"Actual time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Rounded to: {timestamp}")

        # Get weather data or use placeholder values
        if weather_data is None:
            weather_data = {
                "temperature": None,
                "weather_category": "unknown",
                "is_raining": "unknown",
                "is_daytime": "unknown",
            }

        # Check for duplicate timestamp entries to avoid duplicates
        should_append = True
        if os.path.exists(self.csv_path):
            with open(self.csv_path, "r", newline="") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if row and row[0] == timestamp:
                        should_append = False
                        print(f"Skipping duplicate entry for timestamp {timestamp}")
                        break

        # Append the new row to the CSV if not a duplicate
        if should_append:
            with open(self.csv_path, "a", newline="\n") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        timestamp,
                        visitor_count,
                        weather_data.get("temperature"),
                        weather_data.get("weather_category", "unknown"),
                        weather_data.get("is_raining", "unknown"),
                        weather_data.get("is_daytime", "unknown"),
                        is_holiday,
                        is_vacation,
                        special_name,
                    ]
                )

            # Properly formatted result log
            print(
                f"Data saved: {timestamp}, {visitor_count} visitors, "
                f"{weather_data.get('temperature')}°C, {weather_data.get('weather_category')}, "
                f"Rain: {weather_data.get('is_raining')}, "
                f"Daytime: {weather_data.get('is_daytime')}, "
                f"Holiday: {is_holiday}, Vacation: {is_vacation}"
            )

        return {
            "timestamp": timestamp,
            "count": visitor_count,
            "temperature": weather_data.get("temperature"),
            "weather_category": weather_data.get("weather_category", "unknown"),
            "is_raining": weather_data.get("is_raining", "unknown"),
            "is_daytime": weather_data.get("is_daytime", "unknown"),
            "is_holiday": is_holiday,
            "is_vacation_period": is_vacation,
            "special_date_name": special_name,
        }

    # Keep the old method for backward compatibility
    def store_visitor_count(self, count, weather_data=None):
        """Store a visitor count with timestamp on exact 15 min interval"""
        return self.store_data(count, weather_data)

import os
import datetime
import csv
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, data_dir="data", csv_file="visitor_counts.csv"):
        self.data_dir = data_dir
        self.csv_path = os.path.join(data_dir, csv_file)
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Create the data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)

        # Create CSV with headers if it doesn't exist
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "visitor_count"])

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

    def store_visitor_count(self, count):
        """Store a visitor count with timestamp on exact 15 min interval"""
        now = datetime.datetime.now()

        # Round to nearest 15-minute interval
        rounded_time = self._round_to_15min_interval(now)
        timestamp = rounded_time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Actual time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Rounded to: {timestamp}")

        # Simply append the new row to the CSV
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, count])

        return {"timestamp": timestamp, "count": count}

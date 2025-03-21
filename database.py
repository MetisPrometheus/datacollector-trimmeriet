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

    def store_visitor_count(self, count):
        """Store a visitor count with the current timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Storing visitor count {count} at {timestamp}")

        # Simply append the new row to the CSV
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, count])

        return {"timestamp": timestamp, "count": count}

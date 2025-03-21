import requests
from bs4 import BeautifulSoup
import time
import datetime
import logging
import pandas as pd
import os
from pathlib import Path
import psutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("visitor_count.log"), logging.StreamHandler()],
)

# CSV file setup
CSV_FILE = "visitor_counts.csv"
CSV_COLUMNS = ["timestamp", "visitor_count"]


def fetch_visitor_count():
    """Scrape the visitor count from the Xakt website"""
    url = "https://medlem.xakt.no/MinSide/Home/VisitorStatistics?org=818598912"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the div with the visitor count
        visitor_element = soup.select_one('div[style="font-size: 2rem;"]')
        if visitor_element:
            visitor_count = int(visitor_element.text.strip())
            return visitor_count

    except Exception as e:
        logging.error(f"Error fetching visitor data: {e}")
        return None


def initialize_csv():
    """Create the CSV file with headers if it doesn't exist"""
    if not Path(CSV_FILE).exists():
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(CSV_FILE, index=False)
        logging.info(f"Created new CSV file: {CSV_FILE}")


def save_to_dataframe(timestamp, visitor_count):
    """Save the data to a pandas DataFrame and then to CSV"""
    # Create a new row as a DataFrame
    new_data = pd.DataFrame(
        {"timestamp": [timestamp], "visitor_count": [visitor_count]}
    )

    # If the file exists, append to it
    if os.path.exists(CSV_FILE):
        # Read existing data
        try:
            df = pd.read_csv(CSV_FILE)
            # Append new data
            df = pd.concat([df, new_data], ignore_index=True)
            # Save back to CSV
            df.to_csv(CSV_FILE, index=False)
        except Exception as e:
            logging.error(f"Error appending to CSV: {e}")
            # Fallback to direct append
            new_data.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        # Create new file with header
        new_data.to_csv(CSV_FILE, index=False)

    logging.info(f"Saved data to {CSV_FILE}")


def job():
    """Function to run every minute"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Running job at {current_time}")

    visitor_count = fetch_visitor_count()
    if visitor_count is not None:
        logging.info(f"Current visitor count: {visitor_count}")
        save_to_dataframe(current_time, visitor_count)
    else:
        logging.warning("Failed to retrieve visitor count")


def wait_until_next_minute():
    """Wait until the start of the next minute"""
    now = datetime.datetime.now()

    # Create target time (next minute with seconds = 0)
    if now.second == 0:
        # If we're already at exactly XX:XX:00, wait until the next minute
        target_time = now.replace(second=0) + datetime.timedelta(minutes=1)
    else:
        # Otherwise wait until the next minute
        target_time = now.replace(second=0) + datetime.timedelta(minutes=1)

    # Calculate wait time in seconds
    wait_seconds = (target_time - now).total_seconds()

    logging.info(f"Current time: {now.strftime('%H:%M:%S')}")
    logging.info(f"Target time: {target_time.strftime('%H:%M:%S')}")
    logging.info(f"Waiting {wait_seconds:.2f} seconds until next minute...")

    # Add a small buffer to ensure we're truly in the next minute
    time.sleep(wait_seconds + 0.1)


def create_lock_file():
    """Create a lock file to prevent multiple instances from running - Windows compatible"""
    lock_file = "visitor_tracker.lock"

    # Check if the lock file exists
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r") as f:
                pid = int(f.read().strip())

            # Check if process is running using psutil (cross-platform way)
            if psutil.pid_exists(pid):
                logging.error(
                    f"Another instance is already running with PID {pid}. Exiting."
                )
                return False
            else:
                logging.warning(
                    f"Process with PID {pid} is not running. Removing stale lock file."
                )
                os.remove(lock_file)
        except (ValueError, IOError) as e:
            logging.warning(f"Invalid lock file. Removing: {e}")
            os.remove(lock_file)

    # Create the lock file with our PID
    try:
        with open(lock_file, "w") as f:
            f.write(str(os.getpid()))
        return True
    except IOError as e:
        logging.error(f"Failed to create lock file: {e}")
        return False


def remove_lock_file():
    """Remove the lock file on exit"""
    lock_file = "visitor_tracker.lock"
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            logging.info("Lock file removed")
        except IOError as e:
            logging.error(f"Failed to remove lock file: {e}")


if __name__ == "__main__":
    # Check if another instance is running
    if not create_lock_file():
        exit(1)

    # Initialize the CSV file if it doesn't exist
    initialize_csv()

    # Track the last execution time to prevent duplicate runs
    last_execution_minute = -1

    logging.info("Visitor count tracking started. Press Ctrl+C to exit.")

    try:
        # Run continuously, on every minute
        while True:
            # Wait until the start of the next minute
            wait_until_next_minute()

            # Get current minute and check if we already ran in this minute
            current_minute = datetime.datetime.now().minute

            if current_minute != last_execution_minute:
                # Run the job
                job()
                # Update the last execution minute
                last_execution_minute = current_minute
            else:
                logging.warning(
                    f"Skipping execution - already ran in minute {current_minute}"
                )

            # Small delay to prevent tight loop
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        # Don't exit on error, try to continue
    finally:
        # Always remove the lock file on exit
        remove_lock_file()

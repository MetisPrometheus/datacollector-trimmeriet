import time
import threading
import schedule
import logging
from scraper import fetch_visitor_count
from database import Database

logger = logging.getLogger(__name__)


class VisitorCountScheduler:
    def __init__(self, interval_minutes=15):
        self.interval_minutes = interval_minutes
        self.db = Database()
        self.stop_event = threading.Event()
        self.thread = None

    def fetch_and_store(self):
        """Fetch visitor count and store in database"""
        logger.info("Running scheduled visitor count fetch")
        count = fetch_visitor_count()
        if count is not None:
            self.db.store_visitor_count(count)
        else:
            logger.warning("Failed to fetch visitor count")

    def run_scheduler(self):
        """Run scheduler in a loop until stopped"""
        schedule.every(self.interval_minutes).minutes.do(self.fetch_and_store)

        # Run once immediately
        self.fetch_and_store()

        while not self.stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        """Start the scheduler in a background thread"""
        if self.thread is not None and self.thread.is_alive():
            logger.warning("Scheduler is already running")
            return

        logger.info(f"Starting scheduler with {self.interval_minutes} minute interval")
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run_scheduler)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the scheduler"""
        if self.thread is not None and self.thread.is_alive():
            logger.info("Stopping scheduler")
            self.stop_event.set()
            self.thread.join(timeout=5)
        else:
            logger.warning("Scheduler is not running")

from scraper import fetch_visitor_count
from database import Database


def main():
    # Initialize database
    db = Database()

    # Fetch visitor count
    visitor_count = fetch_visitor_count()

    if visitor_count is not None:
        # Store in database
        db.store_visitor_count(visitor_count)
        print(f"Successfully stored visitor count: {visitor_count}")
    else:
        print("Failed to fetch visitor count")


if __name__ == "__main__":
    main()

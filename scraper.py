import requests
from bs4 import BeautifulSoup


def fetch_visitor_count():
    """Scrape the visitor count from the Xakt website"""
    url = "https://medlem.xakt.no/MinSide/Home/VisitorStatistics?org=818598912"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the div with the visitor count
        visitor_element = soup.select_one('div[style="font-size: 2rem;"]')
        if visitor_element:
            visitor_count = int(visitor_element.text.strip())
            return visitor_count
        else:
            print("Visitor count element not found on page")
            return None

    except Exception as e:
        print(f"Error fetching visitor data: {e}")
        return None

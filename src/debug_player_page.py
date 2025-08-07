# src/debug_player_page.py
import sqlite3
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

def get_first_player_url():
    """Gets the URL of the very first player from the database."""
    conn = sqlite3.connect('transfers.db')
    cursor = conn.cursor()
    # Fetch the player_url from the first record in the table
    cursor.execute("SELECT player_url FROM transfers LIMIT 1;")
    record = cursor.fetchone()
    conn.close()
    return record[0] if record else None

def fetch_and_print_html(url):
    """Fetches a single page and prints its full HTML structure."""
    if not url:
        print("❌ No URL found in the database.")
        return

    print(f"Fetching HTML from: {url}")
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        print("✅ Page fetched successfully! Printing HTML blueprint...")
        soup = BeautifulSoup(response.content, 'html.parser')
        # .prettify() makes the HTML readable with proper indentation
        print(soup.prettify())
    else:
        print(f"❌ Failed to fetch page. Status code: {response.status_code}")

if __name__ == "__main__":
    player_url = get_first_player_url()
    fetch_and_print_html(player_url)
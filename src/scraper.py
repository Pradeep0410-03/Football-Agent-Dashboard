# src/scraper.py - Final version that correctly saves URLs
import requests
from bs4 import BeautifulSoup
import sqlite3

URL = "https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1/saison_id/2025"
BASE_URL = "https://www.transfermarkt.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
HEADLINES_TO_IGNORE = {"Transfer record", "No Headline Found"}

def fetch_page(url):
    """Fetches the content of a webpage."""
    print(f"Fetching data from: {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print("✅ Page fetched successfully!")
        return response.content
    return None

def parse_transfers(html_content):
    """Parses HTML to extract transfer data including player URLs."""
    if not html_content: return []

    soup = BeautifulSoup(html_content, 'html.parser')
    transfers_list = []
    club_boxes = soup.find_all("div", class_="box")
    print("\nProcessing club data boxes...")

    for box in club_boxes:
        headline_tag = box.find("h2", class_="content-box-headline")
        headline = headline_tag.text.strip() if headline_tag else "No Headline Found"
        if headline in HEADLINES_TO_IGNORE: continue

        tables = box.find_all('div', class_='responsive-table')
        
        # Process Arrivals
        if len(tables) > 0:
            for row in tables[0].find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > 8:
                    player_link_tag = cells[0].find('a')
                    player_name = player_link_tag.text.strip()
                    player_url = BASE_URL + player_link_tag['href']
                    from_club = cells[7].find('a').get('title', 'N/A') if cells[7].find('a') else 'N/A'
                    fee = cells[8].text.strip()
                    transfers_list.append((player_name, from_club, headline, fee, "Arrival", player_url))

        # Process Departures
        if len(tables) > 1:
            for row in tables[1].find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > 8:
                    player_link_tag = cells[0].find('a')
                    player_name = player_link_tag.text.strip()
                    player_url = BASE_URL + player_link_tag['href']
                    to_club = cells[7].find('a').get('title', 'N/A') if cells[7].find('a') else 'N/A'
                    fee = cells[8].text.strip()
                    transfers_list.append((player_name, headline, to_club, fee, "Departure", player_url))
    
    return transfers_list

def save_to_db(transfers):
    """Saves a list of transfers with URLs into the database."""
    if not transfers:
        print("No transfers to save.")
        return

    conn = sqlite3.connect('transfers.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transfers;")
    
    insert_query = "INSERT INTO transfers (player, from_club, to_club, fee, type, player_url) VALUES (?, ?, ?, ?, ?, ?);"
    cursor.executemany(insert_query, transfers)
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Successfully saved {len(transfers)} transfers (with URLs) to the database.")

if __name__ == "__main__":
    html = fetch_page(URL)
    transfer_data = parse_transfers(html)

    if transfer_data:
        print(f"\n✅ Successfully extracted {len(transfer_data)} transfers!")
        save_to_db(transfer_data)
    else:
        print("\n❌ No transfer data was extracted.")
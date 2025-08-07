# src/agent_scraper.py - LIMITED to 100 players
import sqlite3
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

def get_transfers_without_agents():
    """Fetches a limited number of records from the DB that don't have an agent name yet."""
    conn = sqlite3.connect('transfers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # THIS IS THE CHANGED LINE: We added "LIMIT 100" to the end of the query
    query = "SELECT id, player, player_url FROM transfers WHERE agent_name IS NULL OR agent_name = '' OR agent_name = 'Not Found' OR agent_name = 'No URL' LIMIT 100;"
    cursor.execute(query)
    
    records = cursor.fetchall()
    conn.close()
    return records

def scrape_agent_from_profile(url):
    """Visits a player's profile page and extracts their agent's name."""
    if not url or not isinstance(url, str):
        return "No URL"
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return f"Scrape Failed ({response.status_code})"
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        info_table_rows = soup.find_all("span", class_="info-table__content--regular")
        
        for row in info_table_rows:
            if "Player agent:" in row.text.strip():
                agent_name_tag = row.find_next_sibling('span')
                if agent_name_tag and agent_name_tag.find('a'):
                    return agent_name_tag.find('a').text.strip()
                else:
                    return agent_name_tag.text.strip() if agent_name_tag else "Not Found"

    except requests.exceptions.RequestException as e:
        print(f"  -> Request Error: {e}")
        return "Request Error"

    return "Not Found"

def update_agent_in_db(record_id, agent_name):
    """Updates a specific record in the database with the agent's name."""
    conn = sqlite3.connect('transfers.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE transfers SET agent_name = ? WHERE id = ?;", (agent_name, record_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    records_to_update = get_transfers_without_agents()
    total_records = len(records_to_update)
    
    if total_records == 0:
        print("ℹ️ No new players to scrape agents for. The database is up to date.")
    else:
        print(f"Found {total_records} players without agent information. Starting scrape...")
        for i, record in enumerate(records_to_update):
            agent = scrape_agent_from_profile(record['player_url'])
            update_agent_in_db(record['id'], agent)
            
            print(f"({i+1}/{total_records}) Player: {record['player']} -> Agent: {agent}")
            time.sleep(2) 
    print("\n✅ Agent scraping complete!")
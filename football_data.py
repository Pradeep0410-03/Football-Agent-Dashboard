# football_data.py
import pandas as pd
import os

print("Generating a sample dataset for the dashboard...")

# Define the data as a list of dictionaries
transfers = [
    {'player': 'Declan Rice', 'from': 'West Ham', 'to': 'Arsenal', 'fee': 116.6, 'agent': 'CAA Stellar'},
    {'player': 'Kai Havertz', 'from': 'Chelsea', 'to': 'Arsenal', 'fee': 75.0, 'agent': 'Wasserman'},
    {'player': 'Mason Mount', 'from': 'Chelsea', 'to': 'Man United', 'fee': 64.2, 'agent': 'CAA Base'},
    {'player': 'Moises Caicedo', 'from': 'Brighton', 'to': 'Chelsea', 'fee': 116.4, 'agent': 'Stellar Group'},
    {'player': 'Josko Gvardiol', 'from': 'RB Leipzig', 'to': 'Man City', 'fee': 90.0, 'agent': 'Stellar Group'},
    {'player': 'Andre Onana', 'from': 'Inter Milan', 'to': 'Man United', 'fee': 51.4, 'agent': 'Stellar Group'},
    {'player': 'James Maddison', 'from': 'Leicester', 'to': 'Tottenham', 'fee': 45.6, 'agent': 'CAA Base'}
]

# Create a pandas DataFrame
df = pd.DataFrame(transfers)

# Define the path for the data file inside the 'data' folder
data_path = os.path.join('data', 'transfers.csv')

# Create the 'data' directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Save the DataFrame to a CSV file
df.to_csv(data_path, index=False)

print(f"✅ Clean dataset successfully created at '{data_path}'")
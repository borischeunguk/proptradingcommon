import datetime

import pandas as pd
import json
import os

# Load the JSON file

print(os.getcwd())
product_code = 'AAPL'
fundamental_file_path = f"{product_code}.json"
json_file_path = os.getcwd() + '/../resources/fundamental/' + fundamental_file_path

# Load the JSON data
with open(json_file_path) as f:
    data = json.load(f)

# Extract Earnings History
earnings_history = data['Earnings']['History']

# Convert the extracted data to a DataFrame
earnings_df = pd.DataFrame.from_dict(earnings_history, orient='index')

# Convert index to datetime
earnings_df.index = pd.to_datetime(earnings_df.index)
earnings_df.sort_index(inplace=True)

# Fill missing EPS values with 0 for simplicity
earnings_df['epsActual'].fillna(0, inplace=True)

# Save the DataFrame to a CSV file
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456
csv_file_name = f"results/{product_code}_earnings_history_{timestamp}.csv"
earnings_df.to_csv(csv_file_name)
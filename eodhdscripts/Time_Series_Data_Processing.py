import pandas as pd
import os

# Load the JSON file

print(os.getcwd())
fundamental_file_path = 'AAPL.json'
json_file_path = os.getcwd() + '/../resources/fundamental/' + fundamental_file_path
# data_frame = pd.read_csv(marketdata_file_path, header=None)
data = pd.read_json(json_file_path)

# Convert to DataFrame
df = pd.DataFrame(data)

# Assuming the JSON has a 'date' column, set it as the index
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Sort the DataFrame by date
df.sort_index(inplace=True)

# Display the DataFrame
print(df)
import yfinance as yf
import pandas as pd

# Define the ticker symbol
symbol = "^IRX"

# Download historical market data for S&P 500
sp500_data = yf.download(symbol, start="2016-01-01", end="2024-08-24")

# Save the data to a CSV file
csv_file_name = "3months_tbill_market_data.csv"
sp500_data.to_csv(csv_file_name)

print(f"S&P 500 market data saved to {csv_file_name}")
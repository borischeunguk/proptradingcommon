import yfinance as yf
import pandas as pd

# Define the ticker symbol for US Treasury ETF
symbol = "VUTY.L"

# Download historical market data for VUTY
vuty_data = yf.download(symbol, start="2016-01-01", end="2024-08-24")

# Save the data to a CSV file
csv_file_name = "vuty_market_data.csv"
vuty_data.to_csv(csv_file_name)

print(f"VUTY market data saved to {csv_file_name}")
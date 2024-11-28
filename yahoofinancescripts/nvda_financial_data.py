import yfinance as yf
import pandas as pd

# Define the ticker symbol for NVDA
symbol = "NVDA"

# Download financial data for NVDA
nvda_financials = yf.Ticker(symbol).financials

# Save the data to a CSV file
csv_file_name = "nvda_financials.csv"
nvda_financials.to_csv(csv_file_name)

print(f"NVDA financial data saved to {csv_file_name}")
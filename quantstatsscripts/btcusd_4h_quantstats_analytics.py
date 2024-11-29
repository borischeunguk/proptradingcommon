import matplotlib.pyplot as plt
import quantstats as qs
import pandas as pd
import datetime

from quantstatsscripts.QuantStats_Functions_Util import read_return_csv_file, dataframe_to_series

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock
# stock = qs.utils.download_returns('META')
#
# print(type(stock))
#
# stock.to_csv('stock_returns.csv', header=True)

daily_returns_df = read_return_csv_file('../backtraderscripts/results/backtrader_macd_trailing_sltp_strategy_btcusdt4h_daily_return_20241129_144502.csv')
daily_returns_series = dataframe_to_series(daily_returns_df)
print(type(daily_returns_series))
print(daily_returns_series)

now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456
product_strategy_name = 'backtrader_macd_trailing_sltp_strategy_btcusdt_4h'
daily_return_report_name = f"../backtrader_scripts/reports/{product_strategy_name}_daily_return_report"
daily_return_report_name_timestamp = f'{daily_return_report_name}_{timestamp}.html'
qs.reports.html(daily_returns_series, "BTC-USD", output=daily_return_report_name_timestamp)

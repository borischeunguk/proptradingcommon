import backtrader as bt
import pandas as pd
import os

import logging

from Logger_Config import setup_logger
from BackTrader_Functions_Util import display_dict
from Backtrader_MACD_SLTP_Histogram_MA_Strategy import BacktraderMacdSltpHistogramMaStrategy

# Create a console logger
logger = setup_logger(__name__, log_file='./logs/backtrader_macd_sltp_histogram_ma_strategy_btc_test.log',
                      level=logging.DEBUG)

# 1. Create a subclass of Strategy to define the indicators and logic

# Use Strategy BacktraderCompositeStrategy

# 2. Clean-up and load data using pandas

# Replace 'file_name.csv' with the name of your CSV file
# marketdata_file_path = 'AAPL_Bar_BackTrader_Data.csv'

marketdata_file_path = 'BTC_full_1hour_2013.txt'

marketdata_file_path = 'BTC_full_1hour.txt'

marketdata_file_path = 'BTC_full_1hour_2021_2023.txt'

marketdata_file_path = 'BTC_full_1hour_20230525_20230531.txt'

# Read the CSV file

print(os.getcwd())
marketdata_file_path = os.getcwd() + '/../resources/crypto_full_1hour_u2hwnn8/' + marketdata_file_path

data_frame = pd.read_csv(marketdata_file_path, header=None)
# data_frame = pd.read_csv(marketdata_file_path)

data_frame.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

data_frame['date'] = pd.to_datetime(data_frame['date'])
print(data_frame['date'].dtype)  # This should print datetime64[ns]

data_frame = data_frame.sort_values(by='date')

# Convert 'date' column to datetime and then format it to the desired string format
# data_frame['date'] = pd.to_datetime(data_frame['date'], format='%Y%m%d  %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')

# Display the contents of the DataFrame
# data_frame = data_frame.iloc[:1000]

print(data_frame)

print("Minimum Date:", data_frame['date'].min())
print("Maximum Date:", data_frame['date'].max())

# data_frame.to_csv(marketdata_file_path, index=False)

# 3. Run the strategy with backtrader_scripts and plot the results

data = bt.feeds.PandasData(dataname=data_frame, datetime=0)

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

cerebro.broker.set_cash(1000000)  # Set initial capital to $

cerebro.adddata(data)

# MACD / Macro Trend factors
pfast = 12 # period for the fast moving average
pslow = 26 # period for the slow moving average
psignal = 9 # period for the signal moving average

# cerebro.addstrategy(BacktraderCustomizedIndicator)

# Add the trading strategy
cerebro.addstrategy(BacktraderMacdSltpHistogramMaStrategy,
                    logger=logger,
                    pfast=pfast,
                    pslow=pslow,
                    psignal=psignal)

cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name="timedrawdown")
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="timereturn")

results = cerebro.run(stdstats=True, runonce=False)
# results = cerebro.run()  # run it all

sharpe_ratio = results[0].analyzers.sharpe.get_analysis()
drawdown_info = results[0].analyzers.drawdown.get_analysis()
trade_info = results[0].analyzers.trades.get_analysis()
returns_info = results[0].analyzers.returns.get_analysis()
timedrawdown_info = results[0].analyzers.timedrawdown.get_analysis()
timereturn_info = results[0].analyzers.timereturn.get_analysis()

print('Sharpe Ratio:', sharpe_ratio['sharperatio'])
print('Max Drawdown:', drawdown_info['max']['drawdown'])
print('Total return:', returns_info['rtot'])

print('Average daily return:', returns_info['ravg'])
print('Average monthly return:', returns_info['ravg'] * 21)
print('Average yearly return:', returns_info['ravg'] * 252)

print('PnL per closed trade: \n')
display_dict(trade_info, logger=logger)

print('Average daily time drawdown: \n')
display_dict(timedrawdown_info, logger=logger)

cerebro.plot()  # and plot it with a single command
# cerebro.plot(start=datetime.datetime(2023, 4, 21), end=datetime.datetime(2023, 4, 22))
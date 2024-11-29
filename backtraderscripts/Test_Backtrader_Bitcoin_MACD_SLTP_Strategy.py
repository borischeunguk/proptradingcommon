import datetime

import backtrader as bt
import pandas as pd
import os

import logging

from Backtrader_MACD_SLTP_Strategy import BacktraderMacdSltpStrategy
from Logger_Config import setup_logger
from BackTrader_Functions_Util import display_dict, read_csv_file, extract_and_print_daily_return, \
    extract_and_print_monthly_return

now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456
product_strategy_name = 'backtrader_macd_trailing_sltp_strategy_btcusdt4h'
csv_filename = f"./results/{product_strategy_name}_result"
csv_filename_timestamp = f"{csv_filename}_{timestamp}.csv"  # e.g., report_20240203_123456.csv
logger_filename = f"./logs/{product_strategy_name}_test"
logger_filename_timestamp = f"{logger_filename}_{timestamp}.log"  # e.g., report_20240203_123456.log

# Create a console logger
logger = setup_logger(__name__, log_file=logger_filename_timestamp,level=logging.INFO)

# Read the CSV file

print(os.getcwd())
marketdata_file_path = os.getcwd() + '/../resources/crypto_4hour/btcusdt4h.csv'

data_frame = read_csv_file(marketdata_file_path)
print(data_frame)

data_frame = data_frame[data_frame['date'].dt.year < 2025]
email_notification = False

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
cerebro.addstrategy(BacktraderMacdSltpStrategy,
                    logger=logger,
                    pfast=pfast,
                    pslow=pslow,
                    psignal=psignal)

# Add analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
cerebro.addanalyzer(bt.analyzers.TimeDrawDown, _name="timedrawdown")
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="timereturn")
cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Days, _name="daily_return")
cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Months, _name="monthly_return")

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

extract_and_print_daily_return(results, product_strategy_name, timestamp)
extract_and_print_monthly_return(results, product_strategy_name, timestamp)

cerebro.plot()  # and plot it with a single command
# cerebro.plot(start=datetime.datetime(2023, 4, 21), end=datetime.datetime(2023, 4, 22))
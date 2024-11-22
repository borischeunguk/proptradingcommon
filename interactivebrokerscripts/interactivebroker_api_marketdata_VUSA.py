from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from Logger_Config import setup_logger

import pandas as pd
import threading
import time
import datetime
import logging

# Extra fee maybe required, checking in progress
# https://www.interactivebrokers.co.uk/AccountManagement/AmAuthentication?action=Settings

now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456
logger_filename = 'logs/interactive_broker_historical_market_data'
logger_filename_timestamp = f"{logger_filename}_{timestamp}.log"  # e.g., report_20240203_123456.log

logger = setup_logger(__name__, log_file=logger_filename_timestamp, level=logging.DEBUG)

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.bar_data = []

    def historicalData(self, reqId, bar):
        self.bar_data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume])
        logger.debug(f"HistoricalData. ReqId: {reqId}, Date: {bar.date}, Open: {bar.open}, High: {bar.high}, Low: {bar.low}, Close: {bar.close}, Volume: {bar.volume}")

def save_bar_data_to_csv(bar_data, file_name):
    df = pd.DataFrame(bar_data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df.to_csv(file_name, index=False)
    print(f"Bar data saved to {file_name}")

app = IBapi()
# app.connect('127.0.0.1', 7497, 0)
app.connect('127.0.0.1', 7496, 4001)

# Start the socket in a thread
api_thread = threading.Thread(target=app.run, daemon=True)
api_thread.start()

# Sleep interval to allow time for connection to server
time.sleep(1)

# Define contracts for VUSA and VUTY
contract = Contract()
contract.symbol = "VUSA"
contract.secType = "STK"
contract.exchange = "LSEETF"
contract.currency = "GBP"
# ! [commoditycontract]

# Request historical data
# app.reqMarketDataType(3)

# https://interactivebrokers.github.io/tws-api/historical_limitations.html#pacing_violations

app.reqMarketDataType(2)

duration = '1 Y'
barSize = '1 day'

# The correct format is yyyymmdd hh:mm:ss xx/xxxx where yyyymmdd and xx/xxxx are optional.
# E.g.: 20031126 15:59:00 US/Eastern
# If no date is specified, current date is assumed.
# If no time-zone is specified, local time-zone is assumed(deprecated).
endDateTime = '20241122-00:00:00' # UTC time used

# app.reqHistoricalData(1, contract, '20240415 00:00:00 US/Eastern', '3 D', '1 hour', 'BID_ASK', 0, 1, False, [])
app.reqHistoricalData(1, contract, endDateTime, duration, barSize, 'BID_ASK', 0, 1, False, [])

# Sleep interval to allow time for data to be fetched
time.sleep(60)

durationStr = duration.replace(' ', '')
barSizeStr = barSize.replace(' ', '')
endDateTimeStr = endDateTime.replace('-', '_').replace(':', '')
market_data_file_name = f'../resources/{contract.symbol}_{barSizeStr}_{durationStr}_Market_Data_{endDateTimeStr}_{timestamp}.csv'

save_bar_data_to_csv(app.bar_data, market_data_file_name)

# save_bar_data_to_csv(app.bar_data, 'AAPL_Bar_Data.csv')

# Disconnect from the server, dummy
app.disconnect()


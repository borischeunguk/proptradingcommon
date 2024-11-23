from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from Logger_Config import setup_logger

import threading
import time
import datetime
import logging

# Extra entitlement required
# No data received. Check subscription permissions.
# More info: https://interactivebrokers.github.io/tws-api/fundamentals.html

now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456
logger_filename = 'logs/interactive_broker_fundamental_data'
logger_filename_timestamp = f"{logger_filename}_{timestamp}.log"  # e.g., report_20240203_123456.log

logger = setup_logger(__name__, log_file=logger_filename_timestamp, level=logging.DEBUG)

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.bar_data = []

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

contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

# Request fundamental data
fundamental_data = app.reqFundamentalData(4001, contract, 'Ratios', [])

# Print the data
if fundamental_data:
    print(fundamental_data)
else:
    print("No data received. Check subscription permissions.")

# Disconnect from the server, dummy
app.disconnect()
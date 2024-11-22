from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7497, 123)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server


#Create contract object
apple_contract = Contract()
apple_contract.symbol = 'AAPL'
apple_contract.secType = 'STK'
apple_contract.exchange = 'SMART'
apple_contract.currency = 'USD'

# app.reqMarketDataType(3)
# app.reqHistoricalData(1, apple_contract,'', '2 D', '1 hour', 'BID', 0, 2, False, [])

# # Create contract object
# eurusd_contract = Contract()
# eurusd_contract.symbol = 'GBP'
# eurusd_contract.secType = 'CASH'
# eurusd_contract.exchange = 'IDEALPRO'
# eurusd_contract.currency = 'USD'
#
# # Request historical candles
# app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])

btc_contract = Contract()
btc_contract.symbol = 'ETH'
btc_contract.secType = 'CRYPTO'
btc_contract.exchange = 'PAXOS'
btc_contract.currency = 'USD'

app.reqMarketDataType(3)
app.reqHistoricalData(1, btc_contract, '', '9 D', '1 hour', 'BID', 0, 2, False, [])

time.sleep(5)  # sleep to allow enough time for data to be returned
app.disconnect()
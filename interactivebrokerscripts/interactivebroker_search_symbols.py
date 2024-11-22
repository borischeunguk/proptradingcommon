from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import *  # @UnusedWildImport

import threading
import time

# Documentation:https://interactivebrokers.github.io/tws-api/matching_symbols.html
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.symbols = []

    def symbolSamples(self, reqId: int, contractDescriptions: ListOfContractDescription):
        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += derivSecType + " "
            print("Symbol: ", contractDescription.contract.symbol,
                  "SecType: ", contractDescription.contract.secType,
                  "Currency: ", contractDescription.contract.currency,
                  "Exchange: ", contractDescription.contract.exchange,
                  "PrimaryExchange: ", contractDescription.contract.primaryExchange,
                  "DerivativeSecTypes: ", derivSecTypes)
            self.symbols.append(contractDescription.contract.symbol)

def run_loop():
    app.run()

app = IBapi()
# app.connect('127.0.0.1', 7497, 123)
app.connect('127.0.0.1', 7496, 4001)


# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server

# Request matching symbols
app.reqMatchingSymbols(1, "VUSA")

time.sleep(5)  # Sleep interval to allow time for incoming data
app.disconnect()
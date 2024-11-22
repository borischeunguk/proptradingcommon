from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import time

# https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/
class IBapi(EWrapper, EClient):
     def __init__(self):
         EClient.__init__(self, self)

app = IBapi()

# Confirm that "Enable ActiveX and Socket EClients" is enabled,
# and connection port is the same as "Socket Port" on the TWS "Edit->Global Configuration...->API->Settings" menu.
# Live Trading ports: TWS: 7496; IB Gateway: 4001.
# Simulated Trading ports for new installations of version 954.1 or newer:  TWS: 7497; IB Gateway: 4002

app.connect('127.0.0.1', 7496, 4001)
# app.connect('127.0.0.1', 7497, 123)

# app.run()

#Uncomment this section if unable to connect
#and to prevent errors on a reconnect
time.sleep(2)
app.disconnect()

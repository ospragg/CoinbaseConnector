import sys
sys.path.append('../')

"""
#from coinbaseconnector import CoinbaseWebsocket
from coinbaseconnector.coinbase_websocket import CoinbaseWebsocket
cw = CoinbaseWebsocket()
"""

from coinbaseconnector.connector import CoinbaseConnector


cc = CoinbaseConnector()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import time
import credentials

from coinbaseconnector.cc_websocket import Websocket
from coinbaseconnector.cc_connector import Connector

url="https://api-public.sandbox.pro.coinbase.com"
#url = "wss://ws-feed-public.sandbox.pro.coinbase.com"
url = "wss://ws-feed.pro.coinbase.com/"


cc = Connector(rest_url="https://api-public.sandbox.pro.coinbase.com",
				 websocket_url="wss://ws-feed-public.sandbox.pro.coinbase.com",
				 product="BTC-USD",
				 api_key=credentials.api_key,
				 api_secret=credentials.api_secret,
				 api_passphrase=credentials.api_passphrase)

"""
cc = Connector(rest_url="https://api-public.sandbox.pro.coinbase.com",
				 #websocket_url="wss://ws-feed-public.sandbox.pro.coinbase.com",
				 websocket_url="wss://ws-feed.pro.coinbase.com",
				 product="BTC-EUR",
				 api_key="",
				 api_secret="",
				 api_passphrase="")
"""
cc.start()

for i in xrange(0, 10):
	print str(cc.get_last_ticker())
	time.sleep(1.0)

cc.stop()





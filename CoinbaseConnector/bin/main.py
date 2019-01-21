#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import time

from coinbaseconnector.cc_websocket import Websocket
from coinbaseconnector.cc_connector import Connector

url="https://api-public.sandbox.pro.coinbase.com"
#url = "wss://ws-feed-public.sandbox.pro.coinbase.com"
url = "wss://ws-feed.pro.coinbase.com/"

"""
cc = Connector(rest_url="https://api-public.sandbox.pro.coinbase.com",
				 websocket_url="wss://ws-feed-public.sandbox.pro.coinbase.com",
				 product="BTC-USD",
				 api_key="a2ea00700c9d0f1929bec91dd1facefd",
				 api_secret="nQ9Lm7XeFJnejaYctFcj31INH9IU2dVWMx9xvxPuYetH7v7c8svQISX+lG9OwIyXGbh11vyQwqsDdKapX0zVJQ==",
				 api_passphrase="5jgxgptgky6")
"""
cc = Connector(rest_url="https://api-public.sandbox.pro.coinbase.com",
				 #websocket_url="wss://ws-feed-public.sandbox.pro.coinbase.com",
				 websocket_url="wss://ws-feed.pro.coinbase.com",
				 product="BTC-EUR",
				 api_key="",
				 api_secret="",
				 api_passphrase="")

cc.start()

for i in xrange(0, 10):
	print str(cc.get_last_ticker())
	time.sleep(1.0)

cc.stop()





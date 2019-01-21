#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import time
import credentials

from coinbaseconnector.cc_websocket import Websocket
from coinbaseconnector.cc_connector import Connector

url="https://api-public.sandbox.pro.coinbase.com"
url = "wss://ws-feed-public.sandbox.pro.coinbase.com"
#url = "wss://ws-feed.pro.coinbase.com/"
product = "BTC-USD"

# initialise the websocket
print "Initialising websocket..."
cc = Connector(rest_url="https://api-public.sandbox.pro.coinbase.com",
				 websocket_url="wss://ws-feed-public.sandbox.pro.coinbase.com",
				 product=product,
				 api_key=credentials.api_key,
				 api_secret=credentials.api_secret,
				 api_passphrase=credentials.api_passphrase)

# start the websocket
print "Starting websocket..."
cc.start()

# check data from the websocket
for i in xrange(0, 10):
	print "Getting ticker..."
	print str(cc.get_current_rate())
	time.sleep(1.0)

# place an order
print "Placing order..."
order_response = cc.place_order(product_id=product,
                   side="buy",
                   size="0.05",
                   type="market")
print str(order_response)

# stop the websocket
print "Stopping websocket..."
cc.stop()





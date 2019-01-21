#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time

import sys
sys.path.append('../')
from coinbaseconnector.cc_websocket import Websocket

class TestBasicFunction(unittest.TestCase):
	def setUp(self):
		pass
 
	def test_1(self):
		
		# initialise the websocket
		self.ws = Websocket(url="wss://ws-feed-public.sandbox.pro.coinbase.com",
		                           product="BTC-USD",
		                           channels=["ticker"])
		
		# start and stop the websocket, and make sure we got at least one message
		self.ws.start()
		time.sleep(2.0)
		self.ws.stop()
		self.assertTrue(len(self.ws.pop_messages()) > 0)
 
if __name__ == '__main__':
	unittest.main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import responses

import sys
sys.path.append('../')
from coinbaseconnector.cc_connector import Connector

class TestBasicFunction(unittest.TestCase):
	def setUp(self):
		
		# initialise the connector
		self.con = Connector(rest_url="https://api-public.sandbox.pro.coinbase.com",
		                           websocket_url="wss://ws-feed-public.sandbox.pro.coinbase.com",
		                           product="BTC-USD")
 
	def test_1(self):
		
		# request some candles, and make sure we got some
		candles = self.con._make_request_("GET", "/products/BTC-USD/candles", params={"granularity" : 60}, data={})
		self.assertTrue(len(candles) > 0)
	
	@responses.activate
	def test_2(self):
		
		# set the api auth details so we don't get an assertion error
		self.con.api_key = "api_key"
		self.con.api_secret = "api_secret"
		self.con.api_passphrase = "api_passphrase"
		
		# mock a successful response to a POST request to place an order
		mock_response = {'status': 'pending',
		'post_only': False,
		'product_id':
		'BTC-USD',
		'fill_fees': '0.0000000000000000',
		'funds': '42161.0627574200000000',
		'created_at': '2019-01-21T21:26:53.741208Z',
		'executed_value': '0.0000000000000000',
		'id': u'515e0428-79a8-4752-b34d-3cec4035596a',
		'stp': 'dc',
		'settled': False,
		'filled_size': '0.00000000',
		'type': 'market',
		'side': 'buy',
		'size': '0.05000000'}
		responses.add(responses.POST,
		              "https://api-public.sandbox.pro.coinbase.com/orders",
		              json=mock_response,
		              status=200)
		
		# test the order placing method
		order_response = self.con.place_order(product_id="BTC-USD",
                   side="buy",
                   size="0.05",
                   type="market")
		
		# check that the method worked ok
		self.assertTrue(order_response == mock_response)
 
if __name__ == '__main__':
	unittest.main()
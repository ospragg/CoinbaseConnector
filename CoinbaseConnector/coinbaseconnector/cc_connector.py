#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from cc_websocket import Websocket
import requests
import time
import utils
import urllib
import json


class Connector:
	def __init__(self,
				 rest_url="",
				 websocket_url="",
				 product="",
				 api_key="",
				 api_secret="",
				 api_passphrase="",):
		
		# make sure we've got required arguments
		assert(rest_url != "" and websocket_url != "" and product != "")
		
		# set up some variables
		self.product = product
		self.api_key = api_key
		self.api_secret = api_secret
		self.api_passphrase = api_passphrase
		self.rwt = None
		self.last_ticker = None
		self.rest_url = rest_url
		
		# set up an auth object to pass to the requests api
		self.coinbase_auth = utils.CoinbaseAuth(self.api_key,
		                                  self.api_secret,
		                                  self.api_passphrase)
		
		# set up the websocket connection
		self.ws = Websocket(url=websocket_url,
		                    product=self.product,
		                    channels=["ticker"],
		                    api_key=self.api_key,
		                    api_secret=self.api_secret,
		                    api_passphrase=self.api_passphrase,)
	
	def _read_from_websocket_(self):
		
		# infinite loop popping messages off the websocket buffer
		while 1:
			
			# get all the available messages
			msgs = self.ws.pop_messages()
			
			# go through each of the messages
			for m in msgs:
				
				# if we get a websocket error, restart the websocket
				if m["type"] == "websocket_error":
					self.ws.stop()
					time.sleep(1.0)
					self.ws.start()
				
				# if the message is a ticker message, get save it as the last ticker
				if m["type"] == "ticker":
					self.last_ticker = m
			
			# sleep for a short time
			time.sleep(0.1)
	
	def _make_request_(self, verb, endpoint, params={}, data={}):
		
		# assemble the full url
		full_url = self.rest_url + endpoint
		
		# try making a request, throw an error if we get anything worse than a 200 status
		try:
			r = requests.request(verb,
			                     url=full_url,
			                     auth=self.coinbase_auth,
			                     params=params,
			                     data=json.dumps(data),
			                     timeout=10.0)
			r.raise_for_status()
		except Exception as e:
			raise Exception("request '" + verb + " " + full_url + "' failed with error: " + str(e))
		
		# make sure the request returned json
		try:
			r_json = r.json()
		except:
			raise Exception("request '" + verb + " " + full_url + "' failed to convert to json: " + str(r.text))
		
		return r_json
	
	def get_current_rate(self):
		# return the last ticker received from the websocket
		return self.last_ticker
	
	def place_order(self, **order_data):
		
		# make sure we've got some credentials
		assert(self.api_key != "" and self.api_secret != "" and self.api_passphrase != "")
		
		# TODO: make sure all the order parameters are valid
		# make sure the product is included in the parameters
		order_data.update({"product_id" : self.product})
		
		# make the request
		return self._make_request_("POST", "/orders", params={}, data=order_data)
	
	def start(self):
		
		# if we haven't already, start a new read_from_websocket thread
		if not (self.rwt != None and self.rwt.isActive()):
			self.rwt = threading.Thread(target=lambda: self._read_from_websocket_())
			self.rwt.daemon = True
			self.rwt.start()
		
		# start the websocket connection
		self.ws.start()
	
	def stop(self):
		
		# stop the websocket connection
		self.ws.stop()


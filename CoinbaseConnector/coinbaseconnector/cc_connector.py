#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from cc_websocket import Websocket

import time

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
		self.rwt = None
		self.last_ticker = None
		
		# set up the websocket connection
		self.ws = Websocket(url=websocket_url,
		                    product=product,
		                    channels=["ticker"],
		                    api_key=api_key,
		                    api_secret=api_secret,
		                    api_passphrase=api_passphrase,)
	
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
	
	def get_last_ticker(self):
		return self.last_ticker
	
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


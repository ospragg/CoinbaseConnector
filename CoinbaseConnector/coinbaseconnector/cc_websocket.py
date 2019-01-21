#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import utils
import threading
import websocket
import json
import copy

class Websocket:
	def __init__(self,
				 url="",
				 product="",
				 channels=[],
				 api_key="",
				 api_secret="",
				 api_passphrase="",):
		
		# make sure we've got required arguments
		assert(url != "" and product != "" and channels != [])
		
		# make sure we remove any trailing dashes from the URL
		while url[-1] == "/": url = url[:-1]
		
		# set up some placeholders
		self.ws_url = url
		self.wst = None
		self.ws = None
		self.msg_buff = []
		self.api_key = api_key
		self.api_secret = api_secret
		self.api_passphrase = api_passphrase
		
		# set up the websocket parameters
		self.ws_params = {
			"type" : "subscribe",
			"product_ids" : [product],
			"channels" : channels,
		}
	
	def _on_message_(self, ws, msg):
		# add the message to the message buffer
		# note that this method should run as FAST as possible
		self.msg_buff.append(json.loads(msg))
	
	def _on_open_(self, ws):
		pass
	
	def _on_close_(self, ws):
		pass
	
	def _on_error_(self, ws, error):
		# if there's been an error, add an error message to the
		# buffer and kill the websocket thread
		self.msg_buff.append(json.loads({"type" : "websocket_error"}))
		raise Exception("websocket error: " + str(error))
	
	def start(self):
		
		# check if we already have a thread initialised
		# if we do, make sure the websocket is closed so the thread joins the main thread
		if self.wst != None:
			while self.wst.isAlive():
				self.ws.close()
		
		# set up the websocket
		self.ws = websocket.WebSocketApp(self.ws_url,
										 on_message=self._on_message_,
										 on_open=self._on_open_,
										 on_close=self._on_close_,
										 on_error=self._on_error_,
										 header={})
		
		# start the websocket running in a thread
		self.wst = threading.Thread(target=lambda: self.ws.run_forever())
		self.wst.daemon = True
		self.wst.start()
		
		# wait for the websocket to connect
		while self.ws.sock.connected == False:
			time.sleep(0.01)
		
		# subscribe and authenticate
		all_params = copy.copy(self.ws_params)
		if self.api_key != "" and self.api_secret != "" and self.api_passphrase != "":
			all_params.update(utils.generate_auth_headers(
			                      "GET/users/self/verify",
			                      self.api_key,
			                      self.api_secret,
			                      self.api_passphrase))
		self.ws.send(json.dumps(all_params))
	
	def stop(self):
		
		# if the websocket exists, close it
		if self.ws != None:
			self.ws.close()
	
	def pop_messages(self):
		# retreive some data from the buffer, and reset the buffer
		ret_buff = self.msg_buff
		self.msg_buff = []
		return ret_buff
		
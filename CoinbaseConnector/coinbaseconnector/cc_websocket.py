#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import base64
import hmac
import hashlib
import threading
import websocket
import json

def generate_auth_headers(api_key, api_secret, api_passphrase):
	# generation of auth parameters, as defined in the Coinbase API docs
	t_epoch = time.time()
	message = str(t_epoch) + "GET" + "/users/self/verify"
	hmac_key = base64.b64decode(api_secret)
	signature = hmac.new(hmac_key, message, hashlib.sha256)
	signature_b64 = base64.b64encode(signature.digest())
	return {
		"signature" : signature_b64,
		"key" : api_key,
		"passphrase" : api_passphrase,
		"timestamp" : str(t_epoch),
	}

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
		
		# set up the websocket parameters
		self.ws_params = {
			"type" : "subscribe",
			"product_ids" : [product],
			"channels" : channels,
		}
		
		# if we've got auth info, generate and add some auth headers
		#if api_key != "" and api_secret != "" and api_passphrase != "":
		#	self.ws_params.update(generate_auth_headers(api_key, api_secret, api_passphrase))
	
	def _on_message_(self, ws, msg):
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
		self.ws.send(json.dumps(self.ws_params))
	
	def stop(self):
		
		# if the websocket exists, close it
		if self.ws != None:
			self.ws.close()
	
	def pop_messages(self):
		# retreive some data from the buffer, and reset the buffer
		ret_buff = self.msg_buff
		self.msg_buff = []
		return ret_buff
		
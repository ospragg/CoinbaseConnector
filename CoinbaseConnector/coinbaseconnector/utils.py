#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import base64
import hmac
import hashlib
from requests.auth import AuthBase

def generate_auth_headers(message, api_key, secret_key, passphrase):
	timestamp = str(time.time())
	message = timestamp + message
	hmac_key = base64.b64decode(secret_key)
	signature = hmac.new(hmac_key, message, hashlib.sha256)
	signature_b64 = base64.b64encode(signature.digest())
	return {
		'Content-Type': 'Application/JSON',
		'CB-ACCESS-SIGN': signature_b64,
		'CB-ACCESS-TIMESTAMP': timestamp,
		'CB-ACCESS-KEY': api_key,
		'CB-ACCESS-PASSPHRASE': passphrase
	}

class CoinbaseAuth(AuthBase):
	def __init__(self, api_key, api_secret, api_passphrase):
		self.api_key = api_key
		self.api_secret = api_secret
		self.api_passphrase = api_passphrase

	def __call__(self, r):
		message = r.method + r.path_url + r.body
		r.headers.update(generate_auth_headers(message,
		                       self.api_key,
		                       self.api_secret,
		                       self.api_passphrase))
		return r


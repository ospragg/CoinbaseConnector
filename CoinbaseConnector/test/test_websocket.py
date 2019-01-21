#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import sys
sys.path.append('../')
from coinbaseconnector.websocket import Websocket

class TestBasicFunction(unittest.TestCase):
	def setUp(self):
		self.websocket = Websocket()
 
	def test_1(self):
		self.assertTrue(True)
 
if __name__ == '__main__':
	unittest.main()
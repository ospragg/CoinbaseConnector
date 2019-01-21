#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import sys
sys.path.append('../')
from coinbaseconnector.connector import Connector

class TestBasicFunction(unittest.TestCase):
	def setUp(self):
		self.connector = Connector()
 
	def test_1(self):
		self.assertTrue(True)
 
if __name__ == '__main__':
	unittest.main()
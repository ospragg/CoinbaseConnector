#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import time

from coinbaseconnector.cc_websocket import Websocket
from coinbaseconnector.cc_connector import Connector


"""
cc = Connector()

cc.start()


cc.stop()
"""

#url="https://api-public.sandbox.pro.coinbase.com"
#url = "wss://ws-feed.pro.coinbase.com/"
url = "wss://ws-feed-public.sandbox.pro.coinbase.com"

cws = Websocket(url=url,
                product="BTC-USD",
                channels=["ticker"],
                #channels=["full"],
                #channels=["match"],
                api_key="a2ea00700c9d0f1929bec91dd1facefd",
                api_secret="nQ9Lm7XeFJnejaYctFcj31INH9IU2dVWMx9xvxPuYetH7v7c8svQISX+lG9OwIyXGbh11vyQwqsDdKapX0zVJQ==",
                api_passphrase="5jgxgptgky6",)



cws.start()

time.sleep(60.0)

cws.stop()




#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from coinbaseconnector.connector import Connector


cc = Connector()

cc.start()


cc.stop()
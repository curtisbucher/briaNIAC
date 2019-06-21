#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:42:58 2019

@author: curtisbucher
"""

from pyftdi.ftdi import Ftdi
import time

ftdi = Ftdi()
ftdi.open_from_url("ftdi://1027:24596/1")

while(True):
    ftdi.set_bitmode(0x88, Ftdi.BITMODE_CBUS)
    time.sleep(3)
    ftdi.set_bitmode(0x80, Ftdi.BITMODE_CBUS)
    time.sleep(3)
# never actually gets here...
ftdi.close()
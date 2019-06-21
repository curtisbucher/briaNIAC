#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 17:14:49 2019

@author: curtisbucher
"""

from pylibftdi import BitBangDevice

with BitBangDevice('FT232H') as bb:
    bb.direction = 0x0F  # four LSB are output(1), four MSB are input(0)
    bb.port |= 2         # set bit 1
    bb.port &= 0xFE      # clear bit 0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:11:58 2019

Basically, the w
@author: curtisbucher
"""

import newftdi.pyftdi.ftdi as ftdi
import newftdi.pyftdi.gpio as gpio

GPIO = gpio.GpioController()
FTDI = ftdi.Ftdi()

## Searching for FTDI devices matching the FT232H
vendor = FTDI.VENDOR_IDS["ftdi"]
product = FTDI.PRODUCT_IDS["232h"]
data = FTDI.find_all(((vendor,product),))
vid = str(data[0][0])
pid = str(data[0][1])
ser = str(data[0][3])
url = "ftdi://" + vid + ":" + pid + "/" + ser

## Connecting to FTDI device
GPIO.configure(url)
if GPIO.is_connected:
    print("Device Connected!")


GPIO.set_direction(0b1111111111111111, 0xffff)
#print(GPIO.read())

## CBUS then I/o
GPIO.write(0b00000000000000000001)


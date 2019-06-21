#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Apr 12 12:43:52 2019

@author: curtisbucher
"""
import time
import newftdi.pyftdi.gpio as gpio
import newftdi.pyftdi.ftdi as ftdi
import time

GPIO = gpio.GpioController()
FTDI = ftdi.Ftdi()

pixel_clock = 25.175e6  # In Hz
pixel_delay = 1 / pixel_clock  # In seconds for each loop

horizontal_clock = 31.469e3  # In Hz
# The number of pixel clock cycles for each line
hor_pixels = round(pixel_clock / horizontal_clock) ##800
vert_pixels = 524

V_sync = 2
H_sync = 3

red_pin = 3
green_pin = 4
blue_pin = 5

def connect(product_name="232h", vendor_name="ftdi"):
    # Searching for FTDI devices matching the FT232H
    vendor = FTDI.VENDOR_IDS[vendor_name]
    product = FTDI.PRODUCT_IDS[vendor][product_name]

    data = FTDI.find_all(((vendor, product),))

    # If there are no connected devices
    if not data:
        raise ftdi.FtdiError(
            "No matching devices found. Try plugging in module or different product name"
        )

    # Connecting to FTDI device
    vid = str(data[0][0])
    pid = str(data[0][1])
    ser = str(data[0][3])
    url = "ftdi://" + vid + ":" + pid + "/" + ser
    print(url)

    GPIO.configure(url)
    if GPIO.is_connected:
        print("Device Connected!")
        
def set_gpio(pin, value):
    """ Sets the corresponding pin to `value` """
    if value:
        data = 2**pin | GPIO.read()
    else:
        data = ~(2**pin) & GPIO.read()
    GPIO.write(data)


connect()

count = 0
while True:
    count += 1
    if count % (hor_pixels * vert_pixels) == 0:
        count = 0
        
    if count < (2 * vert_pixels):
        set_gpio(V_sync, False)
    else:
        set_gpio(V_sync, True)
        
    if count % hor_pixels < 96:
        set_gpio(H_sync, False)
    else:
        set_gpio(H_sync, True)
        
    time.sleep(pixel_delay)

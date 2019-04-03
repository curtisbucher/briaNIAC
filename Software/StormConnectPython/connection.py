#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 23:47:20 2019

@author: curtisbucher
Reset Arduino before each use. Wait for light to finish flashing
"""
import serial
import time


## Creating Serial Connection
ser = serial.Serial('/dev/cu.usbmodem14101')
##ser.open()

## Creating data bytearray, cannot be larger than 10 due to buffer size. 
data = list(x for x in range(10,255)) * 100
print("Sending: " + str(list(data)))

## Sending Data
time.sleep(2)
ser.write(data)
ser.write(b'\t')

## Receiving Data
ser.timeout = 2
incoming = ser.read_until(terminator = b'\t')[:-1]

print("Receiving: " + str(list(incoming)))

if not incoming:
    print("Error: Nothing received. Try checking connection or resetting arduino")
elif list(incoming) != list(data):
    print("Error: Data Doesn't Match. Check Program, then hardware")
else:
    print("Success: " + str(len(data)) + " bytes sent.")
    
ser.close()


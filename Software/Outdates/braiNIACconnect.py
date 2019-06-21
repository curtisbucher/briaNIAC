#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:11:58 2019

Program for interfacing with the braiNIAC brainfuck computer's main program
EEPROM. It uses the pyftdi library to interface with the FT232H chip.
@author: curtisbucher
"""

import newftdi.pyftdi.ftdi as ftdi
import newftdi.pyftdi.gpio as gpio
import time

GPIO = gpio.GpioController()
FTDI = ftdi.Ftdi()

WE = 6
OE = 7
increment = 4
clear = 5
data_pins = [8, 9, 10, 11, 12, 13, 14, 15]

address = 0
delay_time = 0.1


def connect(product_name="232h", vendor_name="ftdi"):
    ## Searching for FTDI devices matching the FT232H
    vendor = FTDI.VENDOR_IDS[vendor_name]
    product = FTDI.PRODUCT_IDS[vendor][product_name]
    
    data = FTDI.find_all(((vendor, product),))

    ## If there are no connected devices
    if not data:
        raise ftdi.FtdiError(
            "No matching devices found. Try plugging in module or different product name"
        )

    ## Connecting to FTDI device
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

def get_gpio(pin):
    """ Returs the state of `pin"""
    return ((2**pin) & GPIO.read()) != 0
    

def clear_counter():
    """Clears the program counters, by toggling the `clear` pin"""
    global address
    set_gpio(clear, True)
    set_gpio(clear, False)
    address = 0
    time.sleep(delay_time)
    set_gpio(clear, True)
    
def increment_counter():
    """Increments the program counters, by toggling the `increment` pin"""
    global address
    set_gpio(increment, False)
    set_gpio(increment, True)
    address += 1
    time.sleep(delay_time)
    set_gpio(increment, False)
    
def set_counter(new_address):
    """Sets the program counters, by employing increment() and clear()"""
    if new_address > address:
        for x in range(new_address - address):
            increment_counter()
    elif new_address < address:
        clear_counter()
        for x in range(new_address):
            increment_counter()

def load_byte(number):
    """ Loads the number to GPIO `data_pins`."""
    GPIO.set_direction(0xFFFF, 0xFFFF)
    set_gpio(OE, True)
    set_gpio(WE, True)
    
    # Converting number to 8 digit binary string'
    binary = "{0:b}".format(number)
    binary = "0" * (8-len(binary)) + binary
    binary = binary[::-1]
    print(binary)
    for x in range(8):
        set_gpio(data_pins[x], binary[x]=="1")
    
    ## Toggling write
    set_gpio(WE, False)
    time.sleep(delay_time)
    set_gpio(WE, True)
        
def read_byte():
    """ Returns the data at the IO pins."""
    set_gpio(OE, False)
    set_gpio(WE, True)
    
    binary = 0
    for x in range(8):
        if get_gpio(data_pins[x]):
            binary += 2**x
            print("1",end="")
        else:
            print("0",end="")
    print()
            
    return binary
    
def write(data=[]):
    ## Setting pins to output
    GPIO.set_direction(0xFFFF, 0xFFFF)
    GPIO.write(0x0000)

    clear_counter()  
    
    for byte in data:
        load_byte(byte)
        increment_counter()

def read():
    GPIO.set_direction(0xffff, 0xfff)
    GPIO.write(0x0000)
    clear_counter()
    
    print("--------")
    for x in range(10):
        print(read_byte())
        increment_counter()
        #input()

connect()
write([1,2,3,4,5,6,7,8,9,10])
read()
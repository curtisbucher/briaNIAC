#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 23:47:20 2019

@author: curtisbucher
Reset Arduino before each use. Wait for light to finish flashing
"""
import serial
import time
import os

POS = b'\x01'
NEG = b'\x00'


def read(start_addr, end_addr, file=None):
    """Commanding arduino to read data to `file` from ROM from [start_addr]
    to [end_addr].
    """

    # Sending command to arduino uno, as well as 2, 8 bit addresses for start_addr and end_addr respectively
    start_addrA = start_addr//256
    start_addrB = start_addr % 256

    end_addrA = end_addr//256
    end_addrB = end_addr % 256

    ser.write([1, start_addrA, start_addrB, end_addrA, end_addrB])

    # Receiving data from arduino. The size of each transmission is sent in
    # first byte.
    print("yup")
    received = ser.read(size=end_addr - start_addr)
    print("yup2")

    # Indicating that the CPU is ready or more data
    ser.write(POS)

    # Writing received data to file
    received_list = list(received)
    print("Data: ", received_list)

    # Converting to hex to write to file
    received = [hex(x)[2:] for x in received]
    received = ' '.join(received)

    # Converting to hex to write to file
    if file:
        with open(file, "w") as data:
            data.write(received)

    return received_list


def write(start_addr, end_addr, file):
    """Commanding arduino to write data from `file` into ROM from [start_addr]
    to [end_addr].
    """

    # Sending 16 bit addresses and command
    start_addrA = start_addr//256
    start_addrB = start_addr % 256

    end_addrA = end_addr//256
    end_addrB = end_addr % 256

    ser.write([0, start_addrA, start_addrB, end_addrA, end_addrB])

    # Text files are interpreted as hex values whereas other files are just sent as bytes
    if ".txt" in file:
        # Reading data from file to write to ROM
        with open(file, "r") as d:
            data = d.read()

        # Converting from hex string to int list
        data = data.split(' ')
        data = [int(x, 16) for x in data]
        data = data[0:end_addr - start_addr]

    else:
        # Reading data from file to write to ROM
        with open(file, "rb") as d:
            data = d.read()

    # Must be sent in batches of 64, then wait for conformation
    print("\nSending Data...")
    print("-" * (((end_addr-start_addr)//64)+1))
    for a in range(start_addr, end_addr-64, 64):
        ser.write(data[a:a+64])
        ser.read()
        print("*", end="", flush=True)

    ser.write(data[a+64:end_addr])
    if ser.read() == NEG:
        print("*\n", flush=True)

    # Checking Data
    received = read(start_addr, end_addr)

    if received == data:
        accuracy = 100
    else:
        missed = 0
        for x in range(len(received)):
            if received[x] != data[x]:
                missed += 1
        accuracy = int((len(received) - missed)/len(received)*10000)/100

    print("\nBytes Sent:", len(data))
    print("Accuracy:", str(accuracy)+"%")


# Creating Serial Connection
try:
    ser = serial.Serial('/dev/cu.usbmodem14201')
except:
    try:
        ser = serial.Serial('/dev/cu.usbmodem14101')
    except:
        raise(ConnectionError("Device not connected"))
time.sleep(2)

os.system("clear")
print("LightningStorm 0.3.0")
print("--------------------")

# Establishing Connection
print("Connecting...")
ser.write(POS)
if ser.read() != POS:
    raise ConnectionError("Connection Refused")
print("Connected!\n")

while True:
    # Getting user request
    operation = input("Read/Write: ")

    if "read" in operation.lower():
        # Add support for 16 bit addressing
        start_addr = int(input("Start Address: "))
        end_addr = int(input("End Address: "))
        filename = input("File to read to: ")

        read(start_addr, end_addr, filename)

    elif "write" in operation.lower():
        # Add support for 16 bit addressing
        start_addr = int(input("Start Address: "))
        end_addr = int(input("End Address: "))
        filename = input("File to write from (.txt or other): ")

        write(start_addr, end_addr, filename)

    else:
        print("Ending...")
        break

print("\n")
ser.close()

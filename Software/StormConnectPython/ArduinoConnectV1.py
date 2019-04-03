import serial
import time

def toByte(data_string, base):
    """ Converts any type of data to a byte to be sent"""
    intArray = int(data_string, base),
    byteArray = bytes(intArray)

    return byteArray

## Setting up serial connection
ser = serial.Serial('/dev/cu.usbmodem14101')

## Data to be sent
data = [1,2,3,4,4,5,6,7,7,0,3,3,255]
values = bytearray(data)
ser.write(values)

## Reading data
a = ser.read_until(terminator = b'255')

b = ser.read()

## printing data
print("Sending Data...")
print(a.decode('ascii'),end = "\n\n")

print("Bytes Sent: " + str(len(data)))
print("Bytes Received: " + str(b[0]))

new_data = list(a.decode('ascii'))
print(new_data)

## Closing serial connection
ser.close()

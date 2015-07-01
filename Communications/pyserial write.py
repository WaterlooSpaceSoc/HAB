# Program Purpose:
# This program writes a string to the serial port COM1

# To test this, run "pyserial read.py" first, then in other python shell, run "pyserial write.py"
# Serial ports are required on your computer. If your computer doesn't have any then use an emulator.
# Virtual Serial Ports Emulator is pretty decent - http://www.eterlogic.com/Products.VSPE.html

import serial

ser = serial.Serial(0)      # open first serial port
print (ser.name)            # check which port was really used
message = "Hello World"           # Define the message to be sent
ser.write(message.encode()) # Write to the port. Must use .encode() to convert string to bytes
ser.close()                 # close port

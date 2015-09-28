# Program Purpose:
# This program waits for data on serial port COM1, and writes it to the screen

# To test this, run "pyserial read.py" first, then in other python shell, run "pyserial write.py"
# Serial ports are required on your computer. If your computer doesn't have any then use an emulator.
# Virtual Serial Ports Emulator is pretty decent - http://www.eterlogic.com/Products.VSPE.html

import serial

#Code from main loop, spawning thread and waiting for data
ser = serial.Serial(0, timeout=5)  # Open COM1, 5 second timeout
ser.baudrate = 19200

#Initialize the message string
message = ""

#Code from thread reading serial data
while 1:
  tdata = ser.read(500)                 # Read 500 characters
  print (tdata)
  
  if (tdata.__len__() > 0):             # If we have data, add it to the message
    message += tdata.decode("utf-8")    # Decode the bytes in tdata to make a string

  print ("message = \"" + message + "\"")

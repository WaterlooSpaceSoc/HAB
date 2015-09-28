# importing things
from xbee import ZigBee
import serial

# setting serial
ser = serial.Serial('COM4' , 9600)

# setting zigbee
zbee = ZigBee(ser)


while True:
    while True:
        packet = input('Enter Data: ')   # asking for input
        ser.write(packet.encode())       # sending the input
        if packet[-1] == '~':            # checking for escape charicter
            break
    while True:
        serial.timeout = None            # no time out
        x = ser.read()                   # setting recieved to a variable
        print(x)                         # print recieved data
        if x == b'~':                    # looking for escape
            break
    if packet == 'Cutdown~':             # ultimate escape
        break
ser.close()
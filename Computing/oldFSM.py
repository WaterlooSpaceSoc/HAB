# Combination of things done so far into a cycle that runs from state to state. 
# Change while loop for more iterations.
# Change USB ports to the actual assigned ones when plugged in.

import serial
from datetime import datetime
import pprint, pickle
#import picamera
import time

serc = serial.Serial('/dev/ttyUSB0' , 9600)
ser = serial.Serial('/dev/ttyUSB1',9600)
ser.readline()
#camera=picamera.PiCamera()


a = dict()
f = open('file5','wb')
x = 0
c - 0


print ('Welcome to HAB')
state = 1
d = 0

while d < 5:
    if  state == 1:
        #Read in data from humidity, 10 times
        x = 0
        while x < 10:
            x = x + 1
            data = ser.readline()
            s = datetime.now()
            print (s)
            print (data)
            a[s.strftime('%Y/%m/%d %H:%M:%S')] = data

        pickle.dump(a,f)

        print ('This data has been pickled to a file, then the file was closed')
        print (a.items())
        f.close()
        state = 2
        time.sleep(10)
        
    elif state == 2:
        # Read in data from gps
        print ('No gps yet')
        state = 3
        time.sleep(10)
        
    elif state == 3:
        # Take 5 pictures, rewrites each time, uncomment picamera code when camera is connected
        #c = 0
        #while c < 500:
            #c = c+1
            #if (c % 100 == 0):
            #time = datetime.now()
            #camera.capture('image'+ str(x/100)+ time.strftime('%H:%M:%S') +'.jpg')
            #print ('Picture taken')
        print ('No picture taken')    
        state = 4
        time.sleep(10)
        
    elif state == 4:
        # Send and receive messages with a computer
        while True:
            while True:
                packet = input('Enter Data: ')
                serc.write(packet.encode())
                if packet[-1] == '~':
                    break
            while True:
                serial.timeout = None
                x = serc.read()
                print(x)        
                if x == b'~':
                    break
            if packet == 'Cutdown~':
                break
            time.sleep(10)

    d = d + 1

f.close()
serc.close()
ser.close()

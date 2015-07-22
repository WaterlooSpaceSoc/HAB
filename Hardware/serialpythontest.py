##
##To be used in conjunction with serialpythontest.ino
##
##A simple test that allows Python to read in sensor data readings from the Arduino over serial.
##


import serial

ser = serial.Serial('/dev/ttyUSB1', 9600)

while True:

    #testwrite = ser.read()

    #print(testwrite)
    line = ser.readline()

    print(line)
    print(len(line))

    a = 0

    line = line.decode("utf-8")
    
    while (a < len(line)):
        currval = line[a]
        #currval = str(currval)
        #currval = chr(currval)
        #currval = str(currval)
        print(currval)
        if (currval == "V"):
            print("FOUND V")
            a = a + 1
            ##Then it's altitude
            b = len(line) - 1
            while (b >= 0): ##Moving backwards
                #currchar = chr(line[b])
                currchar = line[b]
                if (currchar == "E"):
                    break
                b = b - 1
            if (b <= 0):
                print("Incorrect Serial format given")
            
            #altitude = line[(a + 2):6] ##Going from the "a:" to the end of the message
            #print(altitude)
            #datval = chr(line[a:b])
            datval = line[a:b]
            print("Found data")
            print(datval)
            print(type(datval))
            break
        else:
            a = a + 1

            
    



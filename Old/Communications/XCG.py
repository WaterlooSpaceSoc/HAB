# XBee Communications Platform
# Written for the High Altitude Ballooning Team

from tkinter import *
from xbee import ZigBee
import serial
import threading

# setting serial
ser = serial.Serial('COM4' , 9600)

# setting zigbee
zbee = ZigBee(ser)

def consolePrint(inputString, console):
    console.config(state=NORMAL)
    console.insert(INSERT,inputString + "\n")
    console.config(state=DISABLED)
    console.yview(END)
    
def sendMSG(packet, console):
    packet += '~'
    z = packet.encode() 
    ser.write(z)       # sending the input
    consolePrint(packet, console)
            
def readMSG(ser, console):
    x = ''
    y = ''
    while True:
        ser.timeout = 10                            # no time out
        x = ser.read()                              # setting recieved to a variable
        x = x.decode()
        y += x
        if x == '~':
            consolePrint(y[:-1], console)
            y = ''
            consolePrint("Waiting for a message...", console)
    

def startRead(ser, console):
     x = threading.Thread(target = readMSG, args=(ser,console))   # setting recieved to a variable
     x.start()  
   
#Main Window
main_window = Tk()
main_window.title("XBee Communications Platform")
main_window.geometry("640x400")

#======== Add Widgets ========#

#Console Frame
cnsl_fr = Frame(main_window, padx = "20", pady = "20")
#Console Label
cnsl_lbl = Label(cnsl_fr, text = "Console Output")
#Console Scroll Bars
cnsl_yscroll = Scrollbar(cnsl_fr)
#Console Output Text Box
cnsl_box = Text(cnsl_fr,width="60",height="15", yscrollcommand=cnsl_yscroll.set)
cnsl_yscroll.config(command=cnsl_box.yview)

#Command Label
cmd_lbl = Label(main_window, text = "Input Command")
#Command Input Box
cmd_ent = Entry(main_window)
cmd_ent.bind("<Return>",lambda event:sendMSG(cmd_ent.get(),cnsl_box))

#Send Button
send_btn = Button(main_window, text = "Send", command=lambda:sendMSG(cmd_ent.get(),cnsl_box))
#=============================#

#Pack Everything to the main window (Order matters)
cmd_lbl.pack()
cmd_ent.pack()
send_btn.pack()
cnsl_lbl.pack()
cnsl_fr.pack()
cnsl_yscroll.pack(side="right",fill="y",expand=False)
cnsl_box.pack()
main_window.after(500, lambda:startRead(ser, cnsl_box))
main_window.mainloop()

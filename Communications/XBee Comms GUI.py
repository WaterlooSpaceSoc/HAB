# XBee Communications Platform
# Written for the High Altitude Ballooning Team

from tkinter import *
from xbee import ZigBee
import serial

# setting serial
ser = serial.Serial('COM4' , 9600)

# setting zigbee
zbee = ZigBee(ser)

def consolePrint(inputString, console):
    console.config(state=NORMAL)
    console.insert(INSERT,inputString + "\n")
    console.config(state=DISABLED)
    sendMSG(inputString)
    console.yview(END)
    
def sendMSG(packet):
    ser.write(packet.encode())       # sending the input
    #if packet[-1] == '~':            # checking for escape charicter
        #break   
        
def readMSG(ser, console):
    #while True:
        #serial.timeout = None            # no time out
        #x = ser.read()                   # setting recieved to a variable
    consolePrint('0', console)            # print recieved data
    main_window.after(500, lambda:readMSG(ser, cnsl_box))
        #if x == b'~':                    # looking for escape
            #break 
    
    
#Main Window
main_window = Tk()
main_window.title("XBee Communications Platform")
main_window.geometry("900x600")

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
cmd_ent.bind("<Return>",lambda event:consolePrint(cmd_ent.get(),cnsl_box))

#Send Button
send_btn = Button(main_window, text = "Send", command=lambda:consolePrint(cmd_ent.get(),cnsl_box))
#=============================#

#Pack Everything to the main window (Order matters)
cmd_lbl.pack()
cmd_ent.pack()
send_btn.pack()
cnsl_lbl.pack()
cnsl_fr.pack()
cnsl_yscroll.pack(side="right",fill="y",expand=False)
cnsl_box.pack()

main_window.after(500, lambda:readMSG(ser, cnsl_box))
main_window.mainloop()

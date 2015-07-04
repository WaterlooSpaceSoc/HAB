# Written for the High Altitude Ballooning Team
from tkinter import *

import serial
from HAB.Operations.GroundMP import GroundMP
from HAB.Operations.Logger import Logger

class CommunicationWindow:
    def __init__(self):
        # setting serial
        self.interface = serial.Serial('COM4', 9600)

        self.main_window = None
        self.cmd_ent = None
        self.send_btn = None
        self.cnsl_box = None

        self.logger = Logger(self.consolePrint, "Ground.log")

        self.mp = GroundMP(self.interface, self.logger.log)
        self.buildGUI()

    def buildGUI(self):
        #Main Window
        self.main_window = Tk()
        self.main_window.title("WSS HAB Communications Platform")
        self.main_window.geometry("640x400")

        #======== Add Widgets ========#

        #Console Frame
        cnsl_fr = Frame(self.main_window, padx = "20", pady = "20")
        #Console Label
        cnsl_lbl = Label(cnsl_fr, text = "Console Output")
        #Console Scroll Bars
        cnsl_yscroll = Scrollbar(cnsl_fr)
        #Console Output Text Box
        self.cnsl_box = Text(cnsl_fr,width="60",height="15", yscrollcommand=cnsl_yscroll.set)
        cnsl_yscroll.config(command=self.cnsl_box.yview)

        #Command Label
        cmd_lbl = Label(self.main_window, text = "Input Command")
        #Command Input Box
        self.cmd_ent = Entry(self.main_window)
        self.cmd_ent.bind("<Return>", lambda: self.mp.sendInput(self.cmd_ent.get()))

        #Send Button
        self.send_btn = Button(self.main_window, text = "Send", command=lambda:self.mp.sendInput(self.cmd_ent.get()))
        #=============================#

        #Pack Everything to the main window (Order matters)
        cmd_lbl.pack()
        self.cmd_ent.pack()
        self.send_btn.pack()
        cnsl_lbl.pack()
        cnsl_fr.pack()
        cnsl_yscroll.pack(side="right",fill="y",expand=False)
        self.cnsl_box.pack()
        self.main_window.protocol('WM_DELETE_WINDOW', self.terminate)
        self.main_window.after(500, self.mp.start)
        self.main_window.mainloop()

    def terminate(self):
        self.mp.stop()
        self.logger.terminate()
        self.main_window.destroy()

    def consolePrint(self, inputString):
        self.cnsl_box.config(state=NORMAL)
        self.cnsl_box.insert(INSERT, inputString)
        self.cnsl_box.config(state=DISABLED)
        self.cnsl_box.yview(END)

def main(args):
    window = CommunicationWindow()



if __name__ == '__main__':
    main(sys.argv)

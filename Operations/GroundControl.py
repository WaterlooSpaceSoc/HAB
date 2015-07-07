# Written for the High Altitude Ballooning Team
import threading
from tkinter import *

import serial
import time
from HAB.Operations.Commands import *
from HAB.Operations.GroundMP import GroundMP
from HAB.Operations.Logger import Logger
from HAB.Operations.QueueProcessor import QueueProcessor, QueueMessage, QueueTermination


class GroundControl(QueueProcessor):
    def __init__(self):
        QueueProcessor.__init__(self, Logger(self.consolePrint, "Ground.log"))

        self.interface = serial.Serial('COM4', 9600)

        self.main_window = None
        self.cmd_ent = None
        self.send_btn = None
        self.cnsl_box = None

        self.mp = GroundMP(self, self.interface, self.logger)
        self.execThread = threading.Thread(target=self.operate, daemon=False, name="TaskExecutor")
        self.buildGUI()

    def operate(self):
        self.processQueue()
        self.main_window.event_generate("<<Quit>>")
        raise SystemExit

    # Override
    # message: Instance of QueueMessage
    def interpretMessage(self, message):
        """
        Note: Always use lowercase for comparison
        :type message QueueMessage
        """
        command = message.command.lower()
        args = message.args

        if command == EXIT:
            self.logger.logMessage("Exiting: ", message)
            raise QueueTermination
        elif command == RELAY:
            if len(args) == 0:
                self.logger.logMessage("Relay invalid: ", message)
            else:
                msg = QueueMessage(args[0], args[1:])
                self.logger.logMessage("Relaying: ", msg)
                self.mp.sendQueueMessage(msg)
        elif command == CHECK_CONNECTION:
            self.logger.logMessage("Check Connection: ", message)
            self.mp.sendQueueMessage(QueueMessage(CONFIRM_CONNECTION, [Logger.getTime()]))
        elif command == CONFIRMED_CONNECTION:
            self.logger.logMessage("Confirmed Connection: ", message)
            # Set a status or something
        elif command == UNKNOWN_COMMAND:
            self.logger.logMessage("Balloon Unknown Command: ", message, error=True)
        else:
            self.logger.logMessage("Ground Unknown Command: ", message, error=True)

    def buildGUI(self):
        #Main Window
        self.main_window = Tk()
        self.main_window.title("WSS HAB Communications Platform")
        # Console Frame
        cnsl_fr = Frame(self.main_window)
        # Console Scroll Bars
        cnsl_yscroll = Scrollbar(cnsl_fr)
        # Console Output Text Box
        self.cnsl_box = Text(cnsl_fr, width=100, heigh=30, yscrollcommand=cnsl_yscroll.set, background="black")
        cnsl_yscroll.config(command=self.cnsl_box.yview)
        self.cnsl_box.tag_configure("green", foreground="green")
        self.cnsl_box.tag_configure("red", foreground="red")
        self.cnsl_box.config(state=DISABLED)
        # Command Input Box
        self.cmd_ent = Entry(self.main_window, background="gray14", foreground="green")
        self.cmd_ent.bind("<Return>", lambda text: self.enterCommand(self.cmd_ent))
        # Pack Everything to the main window (Order matters)
        cnsl_fr.pack(fill="both", expand=YES)
        cnsl_yscroll.pack(side="right",fill="y", expand=NO)
        self.cnsl_box.pack(fill="both", expand=YES)
        self.cmd_ent.pack(fill="x", side="bottom")
        self.cmd_ent.focus_set()
        self.main_window.protocol('WM_DELETE_WINDOW', self.terminateQueue)
        self.main_window.after(100, self.start)
        self.main_window.bind('<<Quit>>', lambda x: self.terminate())
        self.main_window.event_add('<<Quit>>', '<Control-Q>')
        self.main_window.mainloop()

    def enterCommand(self, field):
        """
        :type field Entry
        """
        self.mp.relayInput(field.get())
        field.delete(0, END)

    def start(self):
        self.mp.start()
        self.execThread.start()

    def terminateQueue(self):
        self.sendToQueue(QueueMessage("Exit"))

    def terminate(self):
        QueueProcessor.terminate(self)
        self.mp.stop()
        self.main_window.destroy()

    def consolePrint(self, inputString, error=False):
        self.cnsl_box.config(state=NORMAL)
        tag = "green"
        if error:
            tag = "red"
        self.cnsl_box.insert(END, inputString, tag)
        self.cnsl_box.config(state=DISABLED)
        self.cnsl_box.yview(END)

def main(args):
    groundControl = GroundControl()

if __name__ == '__main__':
    main(sys.argv)

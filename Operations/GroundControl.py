# Written for the High Altitude Ballooning Team
import threading
from tkinter import *

from Commands import *
from GroundMP import GroundMP
from Logger import Logger, LogLvl
from QueueProcessor import QueueMessage, QueueTermination, QueueProcessor


class GroundControl(QueueProcessor):
    def __init__(self, port="COM4"):
        QueueProcessor.__init__(self, Logger(self.consolePrint, "Ground.log"), "GC")

        self.main_window = None
        self.cmd_ent = None
        self.send_btn = None
        self.cnsl_box = None

        self.mp = GroundMP(self, port, self.logger)
        self.execThread = threading.Thread(target=self.operate, name="TaskExecutor")
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

        if cmd(command, EXIT):
            self.logger.logMessage(message)
            raise QueueTermination
        elif cmd(command, RELAY):
            if len(args) == 0:
                self.logger.logMessage(message, "Relay invalid: ", LogLvl.ERROR)
            else:
                msg = QueueMessage(args[0], args[1:])
                self.logger.logMessage(msg, "Relaying: ")
                self.mp.sendToQueue(msg)
        elif cmd(command, CHECK_CONNECTION):
            self.logger.logMessage(message)
            self.mp.sendToQueue(QueueMessage(CONFIRM_CONNECTION, [Logger.getTime()]))
        elif cmd(command, CONFIRMED_CONNECTION):
            self.logger.logMessage(message)
            # Set a status or something
        elif cmd(command, CUTDOWN_RESPONSE):
            self.logger.logMessage(message, lvl=LogLvl.SPECIAL)
        elif cmd(command, CONFIRM):
            self.logger.logMessage(message, lvl=LogLvl.SPECIAL)
        elif cmd(command, UNKNOWN_COMMAND):
            self.logger.logMessage(message, "Balloon Unknown Command: ", LogLvl.ERROR)
        elif cmd(command, ERROR):
            self.logger.logMessage(message, lvl=LogLvl.ERROR)
        else:
            self.logger.logMessage(message, "Ground Unknown Command: ", LogLvl.ERROR)

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
        self.cnsl_box.tag_configure(LogLvl.NORMAL, foreground="lawn green")
        self.cnsl_box.tag_configure(LogLvl.ERROR, foreground="red")
        self.cnsl_box.tag_configure(LogLvl.SPECIAL, foreground="turquoise1")
        self.cnsl_box.tag_configure(LogLvl.RADIO, foreground="wheat")
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
        line = field.get()
        # Flag parsing
        if " -s" in line:
            line = line.replace(" -s", "")
            self.mp.sendInput(line)
        else:
            self.mp.relayInput(line)
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

    def consolePrint(self, inputString, lvl):
        self.cnsl_box.config(state=NORMAL)
        tag = lvl
        self.cnsl_box.insert(END, inputString, tag)
        self.cnsl_box.config(state=DISABLED)
        self.cnsl_box.yview(END)

def main(args):
    if(len(args) > 0):
        hab = GroundControl(args[0])
    else:
        hab = GroundControl()

if __name__ == '__main__':
    main(sys.argv[1:])

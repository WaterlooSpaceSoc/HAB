import sys
import threading
import serial
import time
from HAB.Operations.BalloonMP import BalloonMP
from HAB.Operations.Logger import Logger
from HAB.Operations.QueueProcessor import QueueProcessor, QueueMessage, QueueTermination


class BalloonControl(QueueProcessor):
    def __init__(self):
        QueueProcessor.__init__(self, Logger(print, "Balloon.log"))
        self.interface = serial.Serial('COM5', 9600)
        self.mp = BalloonMP(self, self.interface, self.logger)
        self.inFlight = True
        self.operate()

    # Override
    def interpretMessage(self, message):
        """
        Note: Always use lowercase for comparison
        :type message QueueMessage
        """
        command = message.command.lower()

        if command == "exit":
            # DO NOT USE in flight, this commands exits the script. Use Cutdown then find the HAB, after that exit.
            # 2 Step for exit to reduce risk of accidents
            if self.inFlight:
                self.logger.logMessage("Cannot Exit while in flight: ", message)
            else:
                raise QueueTermination
        elif command == "abortflight":
            self.inFlight = False
        elif command == "resumeflight":
            self.inFlight = True
        elif command == "cutdown":
            pass # Do the thing
        else:
            self.logger.logMessage("Unknown Command: ", message)

    def operate(self):
        self.mp.start()
        self.processQueue()
        self.terminate()

    def terminate(self):
        QueueProcessor.terminate(self)
        self.mp.stop()

def main(args):
    hab = BalloonControl()

if __name__ == '__main__':
    main(sys.argv)

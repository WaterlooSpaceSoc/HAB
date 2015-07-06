import sys
import serial
from HAB.Operations.BalloonMP import BalloonMP
from HAB.Operations.Commands import EXIT, ABORT, RESUME, CUTDOWN, RELAY, CONFIRM_CONNECTION, CUTDOWN_RESPONSE
from HAB.Operations.Logger import Logger
from HAB.Operations.QueueProcessor import QueueProcessor, QueueMessage, QueueTermination
from HAB.Operations.ConnectionChecker import ConnectionChecker


class BalloonControl(QueueProcessor):
    def __init__(self):
        QueueProcessor.__init__(self, Logger(lambda line, error=False: sys.stdout.write(line), "Balloon.log"))
        self.interface = serial.Serial('COM5', 9600)
        self.mp = BalloonMP(self, self.interface, self.logger)
        self.cc = ConnectionChecker(self, 30, self.logger)
        self.inFlight = True
        self.operate()

    # Override
    def interpretMessage(self, message):
        """
        Note: Always use lowercase for comparison
        :type message QueueMessage
        """
        command = message.command.lower()
        args = message.args

        if command == EXIT:
            # DO NOT USE in flight, this commands exits the script. Use Cutdown then find the HAB, after that exit.
            # 2 Step for exit to reduce risk of accidents
            if self.inFlight:
                self.logger.logMessage("Cannot Exit while in flight: ", message)
            else:
                self.logger.logMessage("Exiting: ", message)
                raise QueueTermination
        elif command == ABORT:
            self.logger.logMessage("Aborting Flight: ", message)
            self.inFlight = False
        elif command == RESUME:
            self.logger.logMessage("Resuming Flight: ", message)
            self.inFlight = True
        elif command == CUTDOWN:
            self.logger.logMessage("Cutting Down: ", message)
            # Do the thing
            self.sendToQueue(QueueMessage("Relay", [CUTDOWN_RESPONSE, Logger.getTime()] + args))
        elif command == RELAY:
            if len(args) == 0:
                self.logger.logMessage("Relay invalid: ", message)
            else:
                msg = QueueMessage(args[0], args[1:])
                self.logger.logMessage("Relaying: ", msg)
                self.mp.sendQueueMessage(msg)
        elif command == CONFIRM_CONNECTION:
            self.cc.confirm()
            self.logger.logMessage("Confirm Connection: ", message)
            self.sendToQueue(QueueMessage("Relay", ["ConfirmedConnection", Logger.getTime()]))
        else:
            self.logger.logMessage("Unknown Command: ", message)
            self.sendToQueue(QueueMessage("Relay", ["UnknownCommand", message.command] + args))

    def operate(self):
        self.mp.start()
        self.cc.start()
        self.processQueue()
        self.terminate()

    def terminate(self):
        QueueProcessor.terminate(self)
        self.mp.stop()
        self.cc.stop()

def main(args):
    hab = BalloonControl()

if __name__ == '__main__':
    main(sys.argv)

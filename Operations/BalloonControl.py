import sys
from ArduinoMP import ArduinoMP
from BalloonMP import BalloonMP
from Commands import *
from Logger import Logger, LogLvl
from QueueProcessor import QueueProcessor, QueueMessage, QueueTermination
from ConnectionChecker import ConnectionChecker


class BalloonControl(QueueProcessor):
    def __init__(self, port="COM5", inoport="COM6"):
        QueueProcessor.__init__(self, Logger(lambda line, lvl: sys.stdout.write(line), "Balloon.log"), "BC")
        self.mp = BalloonMP(self, port, self.logger)
        self.inomp = ArduinoMP(self, inoport, self.logger)
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

        if cmd(command, EXIT):
            # DO NOT USE in flight, this commands exits the script. Use Cutdown then find the HAB, after that exit.
            # 2 Step for exit to reduce risk of accidents
            if self.inFlight:
                self.logger.logMessage( message, "Cannot Exit while in flight: ")
                self.mp.sendToQueue(QueueMessage("Error", ["In Flight Exit Impossible"]))
            else:
                self.logger.logMessage(message)
                raise QueueTermination
        elif cmd(command, ABORT):
            self.logger.logMessage(message)
            self.mp.sendToQueue(QueueMessage(CONFIRM, ["Flight Aborted"]))
            self.inFlight = False
        elif cmd(command, RESUME):
            self.logger.logMessage(message)
            self.mp.sendToQueue(QueueMessage(CONFIRM, ["Flight Resumed"]))
            self.inFlight = True
        elif cmd(command, CUTDOWN):
            self.logger.logMessage(message, lvl=LogLvl.SPECIAL)
            self.cc.confirm()
            # Do the thing
            self.mp.sendToQueue(QueueMessage(CUTDOWN_RESPONSE, [Logger.getTime()] + args))
        elif cmd(command, RELAY):
            if len(args) == 0:
                self.logger.logMessage(message, "Relay invalid: ")
            else:
                msg = QueueMessage(args[0], args[1:])
                self.logger.logMessage(msg, "Relaying: ")
                self.mp.sendToQueue(msg)
        elif cmd(command, CONFIRM_CONNECTION):
            self.cc.confirm()
            self.logger.logMessage(message)
            self.mp.sendToQueue(QueueMessage(CONFIRMED_CONNECTION, [Logger.getTime()]))
        elif cmd(command, ARDUINO_RESPONSE):
            self.logger.logMessage(message)
            self.mp.sendToQueue(message)
        elif cmd(command, GPS):
            self.logger.logMessage(message)
            self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_GPS]))
        elif cmd(command, HUMIDITY):
            self.logger.logMessage(message)
            self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_HUMIDITY]))
        elif cmd(command, BAROMETER):
            self.logger.logMessage(message)
            self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_BAROMETER]))
        elif cmd(command, TIMESTAMP):
            self.logger.logMessage(message)
            self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_TIMESTAMP]))
        elif cmd(command, ERROR):
            self.logger.logMessage(message)
            self.mp.sendToQueue(message)
        elif cmd(command, PICTURE):
            self.logger.logMessage(message)
            self.mp.sendToQueue(message)
        else:
            self.logger.logMessage(message, "Unknown Command: ")
            self.mp.sendToQueue(QueueMessage(UNKNOWN_COMMAND, [message.command] + args))

    def operate(self):
        self.mp.start()
        self.inomp.start()
        self.cc.start()
        self.processQueue()
        self.terminate()

    def terminate(self):
        QueueProcessor.terminate(self)
        self.mp.stop()
        self.inomp.stop()
        self.cc.stop()

def main(args):
    if(len(args) > 1):
        hab = BalloonControl(args[0], args[1])
    else:
        hab = BalloonControl()

if __name__ == '__main__':
    main(sys.argv[1:])

from Commands import *
from Logger import LogLvl
from MessageProcessor import MessageProcessor, unit_separator


class ArduinoMP(MessageProcessor):
    def __init__(self, main, port, logger):
        MessageProcessor.__init__(self, main, port, logger, name="AMP")

    def sendArduino(self, command):
        self.logger.log("Sending: " + command, LogLvl.RADIO)
        self.interface.write(command.encode())

    def interpretMessage(self, message):
        command = message.command.lower()
        args = message.args
        if cmd(command, ARDUINO_RELAY):
            self.sendArduino(args[0])
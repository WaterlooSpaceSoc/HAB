import time

from Commands import RELAY

null_terminator = '\0'
unit_separator = '\31'

from abc import ABCMeta
import threading
from serial import Serial
from QueueProcessor import QueueMessage, QueueTermination, QueueProcessor
from Logger import LogLvl


class MessageProcessor(QueueProcessor, metaclass=ABCMeta):
    def __init__(self, main, port, logger, baud=9600, name="MP"):
        """
        Message Processsing Class for Serial Communication
        :type main QueueProcessor
        :type port Serial
        :type logger Logger
        """
        QueueProcessor.__init__(self, logger, name)
        self.shutdown = False
        self.main = main
        self.interface = Serial(port, baud, timeout=0.1)
        self.thread = threading.Thread(target=self.processQueue, name="MessageProcessor")

    def start(self):
        self.thread.start()

    def stop(self):
        self.shutdown = True
        self.interface.close()

    def receive(self):
        return self.interface.read().decode()

    # Private
    def send(self, message):
        self.logger.log("Sending: " + message.replace(unit_separator, " "), LogLvl.RADIO)
        self.interface.write(message.encode())

    def sendInput(self, line):
        split = line.split(" ")
        command = split[0]
        args = split[1:]
        self.main.sendToQueue(QueueMessage(command, args))

    def relayInput(self, line):
        split = line.split(" ")
        command = split[0]
        args = split[1:]
        self.main.sendToQueue(QueueMessage(RELAY, [command] + args))

    # Private
    def sendQueueMessage(self, message):
        """
        :type message QueueMessage
        """
        msg = MessageProcessor.buildMessage(message.command, message.args)
        self.send(msg)

    @classmethod
    def buildValue(cls, args):
        value = ""
        for arg in args:
            value += unit_separator + arg
        if value == "":
            return None
        return value

    @classmethod
    def buildMessage(cls, command, args):
        message = command
        value = MessageProcessor.buildValue(args)
        if value is not None:
            message += value
        message += null_terminator
        return message

    def extract(self, message):
        command, args = self.unmarshal(message)
        self.logger.log("Receiving: " + message.replace(unit_separator, " "), LogLvl.RADIO)
        self.execute(command, args)

    def execute(self, command, args):
        message = QueueMessage(command, args)
        self.main.sendToQueue(message)

    def interpretMessage(self, message):
        self.sendQueueMessage(message)

    def processQueue(self):
        while not self.shutdown:
            if self.queue.qsize() == 0:
                time.sleep(0.1)
            else:
                try:
                    self.interpretMessage(self.pop())
                except QueueTermination:
                    break
            self.processReception()
        raise SystemExit

    def processReception(self):
        message = ""
        while not self.shutdown:
            char = self.receive()
            if len(char) == 0:
                break
            elif char == null_terminator:
                self.extract(message)
                break
            else:
                message += char

    def unmarshal(self, message):
        """
        Unmarshal the message into its components.
        Form: "Command:arg1:arg2..." where : is the unit_separator
        """
        # Note this format is prone to change, I needed something to work with
        message = message.replace(null_terminator, "")
        split = message.split(unit_separator)
        return split[0], split[1:]

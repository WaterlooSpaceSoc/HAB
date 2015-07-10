from abc import ABCMeta, abstractmethod
from queue import Queue
import time
from HAB.Operations.Commands import RELAY
from HAB.Operations.Logger import LogLvl


class QueueProcessor(metaclass=ABCMeta):

    def __init__(self, logger, prefix=""):
        self.logger = logger
        self.queue = Queue()
        self.prefix = prefix

    def sendToQueue(self, message):
        if isinstance(message, QueueMessage):
            self.queue.put(message)
            self.logger.logMessage(message, "Insert in " + self.prefix + " Queue: ", LogLvl.SILENT)
        else:
            self.logger.log(self.prefix + " Not a QueueMessage: " + message.__str__(), LogLvl.ERROR)

    def pop(self):
        message = self.queue.get()
        self.logger.logMessage(message, "Pop from " + self.prefix + " Queue: ", LogLvl.SILENT)
        return message

    def processQueue(self):
        while True:
            if self.queue.qsize() == 0:
                time.sleep(0.1)
            else:
                try:
                    self.interpretMessage(self.pop())
                except QueueTermination:
                    break

    # Must be overriden
    @abstractmethod
    def interpretMessage(self, message):
        """
        :type message QueueMessage
        """
        pass

    def terminate(self):
        self.logger.terminate()

class QueueMessage:
    """
    Data structure to hold the Messages accepted by the QueueProcessor
    """
    def __init__(self, command, argsList=list()):
        """
        :type command str
        :type argsList list
        """
        self.command = command
        self.args = argsList

    def getArgs(self):
        return self.args

    def getCommand(self):
        return self.command

    @classmethod
    def Relay(cls, message):
        """
        :type message QueueMessage
        """
        return QueueMessage(RELAY, [message.command] + message.args)

    def __str__(self):
        return self.command + " " + self.args.__str__()

class QueueTermination(BaseException):
    pass

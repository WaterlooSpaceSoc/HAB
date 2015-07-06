from abc import ABCMeta, abstractmethod
from queue import Queue
import time


class QueueProcessor(metaclass=ABCMeta):

    def __init__(self, logger):
        self.logger = logger
        self.queue = Queue()

    def sendToQueue(self, message):
        if isinstance(message, QueueMessage):
            self.queue.put(message)
            self.logger.logMessage("Insert in Queue: ", message)
        else:
            self.logger.log("Not a QueueMessage: " + message.__str__())

    def pop(self):
        message = self.queue.get()
        self.logger.logMessage("Pop from Queue: ", message)
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

    def __str__(self):
        return self.command + " " + self.args.__str__()

class QueueTermination(BaseException):
    pass

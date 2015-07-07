from datetime import datetime
from HAB.Operations.QueueProcessor import QueueMessage

timeFormat = "%H:%M:%S.%f: "
dateFormat = "%Y-%m-%d %H:%M:%S.%f: "

class Logger:
    def __init__(self, output, fileName):
        self.file = open(fileName, 'a', 1)
        self.output = output
        self.file.write("----------------\nStarting Operations: " + datetime.now().strftime(dateFormat) + "\n\n")

    def log(self, message, error=False):
        line = (datetime.now().strftime(timeFormat) + message + "\n")
        self.file.write(line)
        self.output(line, error=error)

    def logMessage(self, prefix, message, error=False):
        """
        :type message QueueMessage
        """
        self.log(prefix + message.__str__(), error=error)

    @classmethod
    def getTime(cls):
        return datetime.now().strftime("%H:%M:%S.%f")

    def terminate(self):
        self.file.write("\nEnding Operations: " + datetime.now().strftime(dateFormat) + "\n----------------\n")
        self.file.close()
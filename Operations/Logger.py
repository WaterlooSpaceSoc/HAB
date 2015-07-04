from datetime import datetime
from HAB.Operations.MessageProcessor import unit_separator

timeFormat = "%H:%M:%S.%f: "
dateFormat = "%Y-%m-%d %H:%M:%S.%f: "

class Logger:
    def __init__(self, output, fileName):
        self.file = open(fileName, 'a')
        self.output = output
        self.file.write("Starting Operations: " + datetime.now().strftime(dateFormat) + "\n\n")

    def log(self, message):
        line = (datetime.now().strftime(timeFormat) + message + "\n").replace(unit_separator, " ")
        self.file.write(line)
        self.output(line)

    def terminate(self):
        self.file.write("\nEnding Operations: " + datetime.now().strftime(dateFormat) + "\n----------------\n\n")
        self.file.close()
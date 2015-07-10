from datetime import datetime

timeFormat = "%H:%M:%S.%f: "
dateFormat = "%Y-%m-%d %H:%M:%S.%f: "

class LogLvl:
    SILENT = "silent"
    NORMAL = "normal"
    ERROR = "error"
    SPECIAL = "special"
    RADIO = "radio"

class Logger:
    def __init__(self, output, fileName):
        self.file = open(fileName, 'a', 1)
        self.output = output
        self.file.write("----------------\nStarting Operations: " + datetime.now().strftime(dateFormat) + "\n\n")

    def log(self, message, lvl=LogLvl.NORMAL):
        line = (datetime.now().strftime(timeFormat) + message + "\n")
        self.file.write(line)
        if lvl != LogLvl.SILENT:
            self.output(line, lvl)

    def logMessage(self, message, prefix="", lvl=LogLvl.NORMAL):
        self.log(prefix + message.__str__(), lvl)

    @classmethod
    def getTime(cls):
        return datetime.now().strftime("%H:%M:%S.%f")

    def terminate(self):
        self.file.write("\nEnding Operations: " + datetime.now().strftime(dateFormat) + "\n----------------\n")
        self.file.close()



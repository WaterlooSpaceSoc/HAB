import threading
import serial

null_terminator = '\0'
unit_separator = '\31'

def buildValue(args):
    value = ""
    for arg in args:
        value += unit_separator + arg
    if value == "":
        return None
    return value

def buildMessage(command, args):
    message = command
    value = buildValue(args)
    if value is not None:
        message += value
    message += null_terminator
    return message

class MessageProcessor:
    def __init__(self, process, interface, log):
        self.shutdown = False
        self.interface = interface
        self.log = log
        self.thread = threading.Thread(target=process)

    def start(self):
        self.thread.start()

    def stop(self):
        self.shutdown = True
        self.interface.close()

    def receive(self):
        return self.interface.read().decode()

    def send(self, message):
        self.log("Sending: " + message)
        self.interface.write(message.encode())

    def sendInput(self, line):
        split = line.split(" ")
        message = buildMessage(split[0], split[1:])
        self.send(message)

    def extract(self, message):
        command, args = self.unmarshal(message)
        self.log("Receiving: " + message)
        self.execute(command, args)

    # Must be overriden
    def execute(self, command, args):
        pass

    def process(self):
        message = ""
        while not self.shutdown:
            self.interface.timeout = 10
            char = self.receive()
            if char == null_terminator:
                self.extract(message)
                message = ""
            else:
                message += char
        raise SystemExit

    def unmarshal(self, message):
        """
        Unmarshal the message into its components.
        Form: "Command:arg1:arg2..." where : is the unit_separator
        """
        # Note this format is prone to change, I needed something to work with
        message = message.replace(null_terminator, "")
        split = message.split(unit_separator)
        return split[0], split[1:]

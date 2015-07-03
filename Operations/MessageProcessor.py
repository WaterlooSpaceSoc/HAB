import threading
import serial

null_terminator = '\0'
unit_separator = '\31'

def buildResponse(command, value="None"):
    return _buildMessage("R", command, value)

def buildCommand(command, value="None"):
    return _buildMessage("C", command, value)

def _buildMessage(header, command, value):
    message = header + unit_separator + command + unit_separator + value + null_terminator
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

    def execute(self, message):
        type, command, args = self.unmarshal(message)
        self.log("Receiving: " + message) # TODO: Something useful

    def process(self):
        message = ""
        while not self.shutdown:
            self.interface.timeout = 10
            char = self.receive()
            if char == null_terminator:
                self.execute(message)
                message = ""
            else:
                message += char
        raise SystemExit

    def unmarshal(self, message):
        """
        Unmarshal the message into its components.
        Form: "X:Command:arg1:arg2..." where : is the unit_separator
        X can be C for command or R for response.
        """
        # Note this format is prone to change, I needed something to work with
        split = message.split(unit_separator)
        return split[0], split[1], split[2:]

class GroundControlMP(MessageProcessor):
    def __init__(self, interface, log):
        MessageProcessor.__init__(self, self.process, interface, log)

class BalloonMP(MessageProcessor):
    def __init__(self, interface, log):
        MessageProcessor.__init__(self, self.process, interface, log)
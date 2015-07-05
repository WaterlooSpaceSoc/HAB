import threading
from HAB.Operations.MessageProcessor import MessageProcessor
from HAB.Operations.QueueProcessor import QueueMessage


class BalloonMP(MessageProcessor):
    def __init__(self, main, interface, logger):
        MessageProcessor.__init__(self, main, interface, logger)
        self.input_thread = threading.Thread(target=self.seekInput, daemon=True)

    def start(self):
        MessageProcessor.start(self)
        self.input_thread.start()

    def seekInput(self):
        while not self.shutdown:
            command = input("")
            # Internal Exit
            if command.lower() == "exit":
                self.main.sendToQueue(QueueMessage(command, list))
            elif command.lower() == "abortflight":
                self.main.sendToQueue(QueueMessage(command, list))
            self.sendInput(command)
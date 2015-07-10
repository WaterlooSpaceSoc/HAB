import threading

from HAB.Operations_old.MessageProcessor import MessageProcessor


class BalloonMP(MessageProcessor):
    def __init__(self, main, port, logger):
        MessageProcessor.__init__(self, main, port, logger)
        self.input_thread = threading.Thread(target=self.seekInput, daemon=True)

    def start(self):
        MessageProcessor.start(self)
        self.input_thread.start()

    def seekInput(self):
        while not self.shutdown:
            command = input("")
            self.sendInput(command)
        raise SystemExit
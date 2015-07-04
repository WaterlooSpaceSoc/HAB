from HAB.Operations.MessageProcessor import MessageProcessor


class BalloonMP(MessageProcessor):
    def __init__(self, interface, log):
        MessageProcessor.__init__(self, self.process, interface, log)
from HAB.Operations.MessageProcessor import MessageProcessor


class GroundMP(MessageProcessor):
    def __init__(self, main, interface, logger):
        MessageProcessor.__init__(self, main, interface, logger)
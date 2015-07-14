import MessageProcessor


class GroundMP(MessageProcessor):
    def __init__(self, main, port, logger):
        MessageProcessor.__init__(self, main, port, logger)
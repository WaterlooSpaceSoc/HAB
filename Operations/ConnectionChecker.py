import threading
from datetime import datetime
import time
from HAB.Operations.Commands import CUTDOWN, RELAY, CHECK_CONNECTION
from HAB.Operations.Logger import Logger
from HAB.Operations.QueueProcessor import QueueProcessor, QueueMessage


class ConnectionChecker:
    def __init__(self, main, interval, logger):
        """
        :type main QueueProcessor
        :type interval int
        :type logger Logger
        """
        self.main = main
        self.interval = interval
        self.logger = logger
        self.shutdown = False
        self.confirmed = True
        self.thread = threading.Thread(target=self.process, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.shutdown = True

    def confirm(self):
        self.confirmed = True

    def sendCheckConnection(self):
        if not self.confirmed:
            self.main.sendToQueue(QueueMessage(RELAY, [CHECK_CONNECTION, Logger.getTime()]))

    def sendCutdown(self):
        self.main.sendToQueue(QueueMessage(CUTDOWN, [Logger.getTime(), "ConnectionChecker"]))

    def process(self):
        while not self.shutdown:
            if self.confirmed:
                self.confirmed = False
                self.sendCheckConnection()
                time.sleep(self.interval/3)
                self.sendCheckConnection()
                time.sleep(self.interval/3)
                self.sendCheckConnection()
                time.sleep(self.interval/3)
            else:
                self.sendCutdown()
                self.stop()
        raise SystemExit



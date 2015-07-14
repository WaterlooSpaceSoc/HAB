import threading
import time

from Commands import CUTDOWN, RELAY, CHECK_CONNECTION
from Logger import Logger
from QueueProcessor import QueueMessage, QueueProcessor


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
        self.thread = threading.Thread(target=self.process)
        self.thread.setDaemon(True)

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
                time.sleep(self.interval)
        raise SystemExit




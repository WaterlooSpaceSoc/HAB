import sys

import serial
from HAB.Operations.BalloonMP import BalloonMP
from HAB.Operations.Logger import Logger
from HAB.Operations.MessageProcessor import buildMessage


class HAB:
    def __init__(self):
        self.interface = serial.Serial('COM5', 9600)
        self.logger = Logger(print, "Balloon.log")
        self.mp = BalloonMP(self.interface, self.logger.log)
        self.operate()

    def operate(self):
        self.mp.start()
        self.sendInput()
        self.terminate()

    def sendInput(self):
        while True:
            command = input("")
            if command == "exit" or command == "Exit":
                break
            self.mp.sendInput(command)

    def terminate(self):
        self.mp.stop()
        self.logger.terminate()

def main(args):
    hab = HAB()

if __name__ == '__main__':
    main(sys.argv)
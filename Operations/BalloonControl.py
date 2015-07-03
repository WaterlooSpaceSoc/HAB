import sys

import serial
from HAB.Operations.Logger import Logger
from HAB.Operations.MessageProcessor import BalloonMP, buildCommand


class HAB:
    def __init__(self):
        self.interface = serial.Serial('COM5', 9600) #DR: Will need to be changed to something like '/dev/ttyUSB0' on the Pi
        self.logger = Logger(print, "BalloonControlLog.log")
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
            message = buildCommand(command)
            self.mp.send(message)
            print("Sending: " + message)

    def terminate(self):
        self.mp.stop()
        self.logger.terminate()

def main(args):
    hab = HAB()

if __name__ == '__main__':
    main(sys.argv)

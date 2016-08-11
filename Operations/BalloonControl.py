
import sys
from ArduinoMP import ArduinoMP
from BalloonMP import BalloonMP
from Commands import *
from Logger import Logger, LogLvl
from QueueProcessor import QueueProcessor, QueueMessage, QueueTermination
from ConnectionChecker import ConnectionChecker

#Update July 21 2016
##Adding in popen for terminal
#from subprocess import popen
import subprocess
import datetime

#import grab_gps ##gps grabbing functions

class BalloonControl(QueueProcessor):
	#def __init__(self, port="COM5", inoport="COM6"):
	def __init__(self, port="/dev/ttyUSB0", inoport="/dev/ttyUSB1"):
		QueueProcessor.__init__(self, Logger(lambda line, lvl: sys.stdout.write(line), "Balloon.log"), "BC")
		self.mp = BalloonMP(self, port, self.logger)
		self.inomp = ArduinoMP(self, inoport, self.logger)
		self.cc = ConnectionChecker(self, 30, self.logger)
		self.inFlight = True
		self.operate()

	# Override
	def interpretMessage(self, message):
		"""
		Note: Always use lowercase for comparison
		:type message QueueMessage
		"""
		command = message.command.lower()
		args = message.args

		if cmd(command, EXIT):
			# DO NOT USE in flight, this commands exits the script. Use Cutdown then find the HAB, after that exit.
			# 2 Step for exit to reduce risk of accidents
			if self.inFlight:
				self.logger.logMessage( message, "Cannot Exit while in flight: ")
				self.mp.sendToQueue(QueueMessage("Error", ["In Flight Exit Impossible"]))
			else:
				self.logger.logMessage(message)
				raise QueueTermination
		elif cmd(command, ABORT):
			self.logger.logMessage(message)
			self.mp.sendToQueue(QueueMessage(CONFIRM, ["Flight Aborted"]))
			self.inFlight = False
		elif cmd(command, RESUME):
			self.logger.logMessage(message)
			self.mp.sendToQueue(QueueMessage(CONFIRM, ["Flight Resumed"]))
			self.inFlight = True
		elif cmd(command, CUTDOWN):
			self.logger.logMessage(message, lvl=LogLvl.SPECIAL)
			self.cc.confirm()
			# Do the thing
			self.mp.sendToQueue(QueueMessage(CUTDOWN_RESPONSE, [Logger.getTime()] + args))
		elif cmd(command, RELAY):
			if len(args) == 0:
				self.logger.logMessage(message, "Relay invalid: ")
			else:
				msg = QueueMessage(args[0], args[1:])
				self.logger.logMessage(msg, "Relaying: ")
				self.mp.sendToQueue(msg)
		elif cmd(command, CONFIRM_CONNECTION):
			self.cc.confirm()
			self.logger.logMessage(message)
			self.mp.sendToQueue(QueueMessage(CONFIRMED_CONNECTION, [Logger.getTime()]))
		elif cmd(command, ARDUINO_RESPONSE):
			self.logger.logMessage(message)
			self.mp.sendToQueue(message)
		elif cmd(command, GPS):
			self.logger.logMessage(message)
			#self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_GPS]))
			#subprocess.Popen(["sudo", "python", "grab_gps.py"], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid, close_fds = True)
			#gps_string = subprocess.check_output("sudo python2 grab_gps.py", shell=True)
			gps_string = subprocess.getoutput("sudo python2 grab_gps.py")
			#gps_string = grab_gps()
			print(gps_string)
			print(type(gps_string))
			self.mp.sendToQueue(QueueMessage(GPS, [gps_string])) ##Will this just work?
			
		elif cmd(command, HUMIDITY):
			self.logger.logMessage(message)
			self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_HUMIDITY]))
		elif cmd(command, BAROMETER):
			self.logger.logMessage(message)
			self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_BAROMETER]))
		elif cmd(command, TIMESTAMP):
			self.logger.logMessage(message)
			self.inomp.sendToQueue(QueueMessage(ARDUINO_RELAY, [ARDUINO_TIMESTAMP]))
		elif cmd(command, ERROR):
			self.logger.logMessage(message)
			self.mp.sendToQueue(message)
		elif cmd(command, PICTURE):
			##Hopefully this won't break everything.
			self.logger.logMessage(message)
			#self.mp.sendToQueue(message)
			timestring = datetime.strptime(datetime.now(), '%H:%M:%S')
	
			print(timestring)
			
			hours = timestring.split(":")[0]
			hours = int(hours)
			minutes = timestring.split(":")[1]
			minutes = int(minutes)
			seconds = timestring.split(":")[2]
			
			print(hours)
			print(minutes)
			print(seconds)
			
			invokehours = int(hours)
			invokeminutes = int(minutes)
			
			picstring = "-f pic_" + hours + "_" + minutes + ".jpg"
			
			#subprocess.call(["sudo", "python", "takepicture.py", "-f", picstring])
			subprocess.Popen(["sudo", "python", "takepicture.py", picstring], shell=False, stdout=subprocess.PIPE, preexec_fn=os.setsid, close_fds = True)
			##^^This should allow us to take a picture in another
			##thread whilst still letting us do other things.
			
			
		else:
			self.logger.logMessage(message, "Unknown Command: ")
			self.mp.sendToQueue(QueueMessage(UNKNOWN_COMMAND, [message.command] + args))

	def operate(self):
		self.mp.start()
		self.inomp.start()
		self.cc.start()
		self.processQueue()
		self.terminate()

	def terminate(self):
		QueueProcessor.terminate(self)
		self.mp.stop()
		self.inomp.stop()
		self.cc.stop()

def main(args):
	if(len(args) > 1):
		hab = BalloonControl(args[0], args[1])
	else:
		hab = BalloonControl()

if __name__ == '__main__':
	main(sys.argv[1:])

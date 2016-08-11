#! /usr/bin/python
# Written by Daniel Richard - danielrichard.net 2016
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading

import subprocess
 
gpsd = None #seting the global variable
 
#os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
#if __name__ == '__main__':
def grab_gps():
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    #while True:
    if (True):
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      #os.system('clear')
      subprocess.call("echo '" + "********************" + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "LAT " + str(gpsd.fix.latitude) + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "LON " + str(gpsd.fix.longitude) + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "TIME " + str(gpsd.utc) + ' + ' + str(gpsd.fix.time) + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "ALT " + str(gpsd.fix.altitude) + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "SPD " + str(gpsd.fix.speed) + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "CLIMB " + str(gpsd.fix.climb) + "' >> gps_log.txt", shell=True)
      subprocess.call("echo '" + "********************" + "' >> gps_log.txt", shell=True)
      print("finished writing to file")
 
      #time.sleep(25) #set to whatever
      returnstring = "*LAT " + str(gpsd.fix.latitude) + "*LON " + str(gpsd.fix.longitude) + "*TIME " + str(gpsd.utc)
      return(returnstring)
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print ("Done.\nExiting.")

##Best multi-line commenting ever.
if False:
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'eps         ' , gpsd.fix.eps
      print 'epx         ' , gpsd.fix.epx
      print 'epv         ' , gpsd.fix.epv
      print 'ept         ' , gpsd.fix.ept
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print
      print 'sats        ' , gpsd.satellites

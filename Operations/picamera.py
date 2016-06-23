import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='filename')
args = parser.parse_args()

filename = args.file

import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(4)
    camera.stop_preview()
    camera.capture(filename)

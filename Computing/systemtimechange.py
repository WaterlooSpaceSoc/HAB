#Time Changing Script
#Finalized June 23rd 2015 to work with string variables (eventually to be taken from serial via arduino).

import os

day = "26"

month = "06"

year = "2015"


hour = "22"

minutes = "12"

day = str(day)
hour = str(hour)
year = str(year)
hour = str(hour)
minutes = str(minutes)

#test = '"sudo date --set' + "\ " + y + year + hour + ":" + '"sudo date --set \ "26 FEB 2015 8:02\"""26 FEB 2015 8:02\"

#test = '"sudo date --set' + '\ "' + x + " " + y + " " + year + " " + hour + ":" + minutes + '\"' + '"'

#print(test)

#testtest = "\"" + x + "\""

#print(testtest)

#os.system ("sudo date --set \"26 FEB 2015 8:02\"")

gpstime = "2013-" + "03-" + "16" + ' ' + "01:" + "55"

gpstime = year + "-" + month + "-" + day + ' ' + hour + ":" + minutes

os.system('sudo date -u --set "%s"' % gpstime)

print ("Hello World")




# open the lx terminal and run this program using python time.py
# or just run it in idle.

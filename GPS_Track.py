#!/usr/bin/python3

import os 
import serial
import pynmea2
from datetime import datetime
import threading
from threading import  Thread
import gpxpy
import gpxpy.gpx
import pandas as pd
from rdp import rdp

#sets the permission of the port
os.chmod("/dev/ttyAMA0", 0o666)
os.system("systemctl stop serial-getty@ttyAMA0.service")

#assigns incoming data to variablee
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=0.5)

#strips the data 
line=ser.readline().strip()

#get the current time, to be used for timestamping the folder,file
now = datetime.now()
currentTime = now.strftime("%H:%M:%S")
currentDate = now.strftime("%d.%m.%Y")

#create new timestamped directory if not existing 
newDirName = now.strftime("%d_%m_%Y-%H%M")
folderpathPre = os.path.join('home','pi','GPS',newDirName)
folderpath = "/" + folderpathPre
if not os.path.isdir(folderpath):
	os.mkdir(folderpath)
	
#assign file names for files to be used
pathGGA = os.path.join(folderpath,'track_raw_GGA.gpx')
pathRED = os.path.join(folderpath,'track_raw_RED.gpx')
pathRDP = os.path.join(folderpath,'track_raw_RDP.gpx')
g= open(pathGGA,"r+")

#print to the console that recording was started on date and time 
print("Recording was started at:", currentTime, "on", currentDate, "\n")

#check if raw file contains basic .gpx structure or not, and write if it doesn't
fileHandleGGA = open (pathGGA,"r" )
lineListGGA = fileHandleGGA.readlines()
stringLinesGGA = ''.join(lineListGGA)
fileHandleGGA.close()
if stringLinesGGA.find("gpx") == -1:
	g.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n <gpx version=\"1.0\">\n \t<trk><name>{Name}</name><trkseg>\n \t</trkseg></trk>\n </gpx> \n".format(Name=newDirName))
	g.close()
	
	
print("Recording...")

#set standard values at which to insert the data 
lineInsert=3
lineinsert2=3

#check if file already contains data and if, get the new line value at which to start insert 
lookup = "trkpt"
myFile = open(pathGGA, "r")
for num, row in enumerate(myFile, 1):
	if "trkpt" in row:
		lineInsert = num
myfile.close()

#as long as there is data
while True:
    line=ser.readline().strip()
    str=line.decode()
	
#if the decoded messages contain the GGA message identifier, do the following 
    if "GGA" in str:
	#use pynmea2 to parse the message 
    	data = pynmea2.parse(str)
	#if the latitude values is not 0 
    	if data.latitude != 0:
		#read everything contained in the file and assign to variable
    		g= open(pathGGA,"r")
    		contents = g.readlines()
    		g.close()

    		#get timestamp
    		DateRecording = now.strftime("%Y-%m-%d")
    		t = datetime.now() 
    		hour = t.hour
    		minute = t.minute
    		second = t.second
    		TimeRecording = "{hour}:{min}:{sec}".format(hour=hour,min=minute,sec=second)
		
		#insert formatted data at certain line 
    		contents.insert(lineInsert, "\t\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{alt}</ele><time>{DateR}T{TimeR}Z</time></trkpt>\n".format(lat=data.latitude,lon=data.longitude,alt=data.altitude, DateR=DateRecording, TimeR=TimeRecording))
	    	g=open(pathGGA, "w")
	    	contents = "".join(contents)
		#write data to file
    		g.write(contents)
	    	g.close()
		#increase the line of insertion by 1
	    	lineInsert= lineInsert + 1
	    	
		#open the raw data file
	    	r=open(pathGGA, "r")
		#parse the raw data file
	    	gpx_file = gpxpy.parse(r)
		#reduce the number of points by a factor of 3 
	    	gpx_file.tracks[0].segments[0].points = gpx_file.tracks[0].segments[0].points[::3]
		#argument 'w' will delete any content of the file and start it in write mode 
	    	r= open(pathRED,"w")
		#write the data 
	    	r.write(gpx_file.to_xml())
	    	r.close()
	    	
	    	rdp=open(pathGGA, "r")
	    	gpx_rdp = gpxpy.parse(rdp)
		#assign lat, long, ele values to array variable
	    	segment1 = gpx_rdp.tracks[0].segments[0]
			coords = pd.DataFrame([
        	{'lat': p.latitude, 
        	'lon': p.longitude, 
         	'ele': p.elevation,
         	'time': p.time} for p in segment1.points])
		coords.set_index('time', drop=True, inplace=True)
		#remove duplicate points
		coords = coords[~coords.index.duplicated()]
		#resample the points to 1s freq
		coords = coords.resample('1S').asfreq()
		#apply the RDP algorithm with an ε of 0.000007
		rdp_coords = rdp(coords[['lon', 'lat']].values, epsilon=0.000007)
		
		#set initial value
		value=int(0)
		rdp_coords = np.asarray(rdp_coords)
		#for all values in gpx file
		for i in range(len(points)):
			#if the gpx coordinate is equal to the RDP residual value
  			if points[i].longitude == rdp_coords[value,0]:
        			rdp_coords[value,0] = points[i].longitude
        			rdp_coords[value,1] = points[i].latitude
        			value=value+int(1)
    		else:
			#mask filtered RDP values to NaN
        		points[i].latitude = "NaN"
        		points[i].longitude = "NaN"
        		points[i].elevation = "NaN"
        		
        	RDP_file = open (pathRDP, 'w')
		#write basic gpx header
		RDP_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n <gpx version=\"1.0\">\n \t<trk><name>Today</name><trkseg>\n \t</trkseg></trk>\n </gpx> \n")
		RDP_file.close()
		
		#for all elements in gpx file
		for i in range(len(points)):
			#if long is not masked, e.g. NaN
    			if points[i].longitude != "NaN":
        			RDP_file = open(pathRDP, 'r')
        			contents = RDP_file.readlines()
        			RDP_file.close()
				#insert value
        			contents.insert(lineinsert2, "\t\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{alt}</ele><time>{time}</time></trkpt>\n".format(lat=points[i].latitude,lon=points[i].longitude,alt=points[i].elevation, time=points[i].time))
        			RDP_file=open(pathRDP, 'w') 
        			contents = "".join(contents)
       				RDP_file.write(contents)
        			RDP_file.close()
				#else: all masked values won't be written
	    	

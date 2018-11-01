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

os.chmod("/dev/ttyAMA0", 0o666)
os.system("systemctl stop serial-getty@ttyAMA0.service")

ser=serial.Serial('/dev/ttyAMA0',9600,timeout=0.5)

line=ser.readline().strip()

now = datetime.now()
currentTime = now.strftime("%H:%M:%S")
currentDate = now.strftime("%d.%m.%Y")
newDirName = now.strftime("%d_%m_%Y-%H%M")
folderpathPre = os.path.join('home','pi','GPS',newDirName)
folderpath = "/" + folderpathPre
if not os.path.isdir(folderpath):
	os.mkdir(folderpath)
pathGGA = os.path.join(folderpath,'track_raw_GGA.gpx')
pathRED = os.path.join(folderpath,'track_raw_RED.gpx')
pathRDP = os.path.join(folderpath,'track_raw_RDP.gpx')
g= open(pathGGA,"r+")

print("Recording was started at:", currentTime, "on", currentDate, "\n")

fileHandleGGA = open (pathGGA,"r" )
lineListGGA = fileHandleGGA.readlines()
stringLinesGGA = ''.join(lineListGGA)
fileHandleGGA.close()
if stringLinesGGA.find("gpx") == -1:
	g.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n <gpx version=\"1.0\">\n \t<trk><name>{Name}</name><trkseg>\n \t</trkseg></trk>\n </gpx> \n".format(Name=newDirName))
	g.close()
	
	
print("Recording...")


lineInsert=3
lineinsert2=3

lookup = "trkpt"
myFile = open(pathGGA, "r")
for num, row in enumerate(myFile, 1):
	if "trkpt" in row:
		lineInsert = num
myfile.close()


while True:
    line=ser.readline().strip()
    str=line.decode()

    if "GGA" in str:
    	data = pynmea2.parse(str)
    	if data.latitude != 0:
    		g= open(pathGGA,"r")
    		contents = g.readlines()
    		g.close()

    		
    		DateRecording = now.strftime("%Y-%m-%d")
    		t = datetime.now() 
    		hour = t.hour
    		minute = t.minute
    		second = t.second
    		TimeRecording = "{hour}:{min}:{sec}".format(hour=hour,min=minute,sec=second)
    					
            
    		contents.insert(lineInsert, "\t\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{alt}</ele><time>{DateR}T{TimeR}Z</time></trkpt>\n".format(lat=data.latitude,lon=data.longitude,alt=data.altitude, DateR=DateRecording, TimeR=TimeRecording))
	    	g=open(pathGGA, "w")
	    	contents = "".join(contents)
    		g.write(contents)
	    	g.close()
	    	lineInsert= lineInsert + 1
	    	
	    	r=open(pathGGA, "r")
	    	gpx_file = gpxpy.parse(r)
	    	gpx_file.tracks[0].segments[0].points = gpx_file.tracks[0].segments[0].points[::3]
	    	r= open(pathRED,"w")
	    	r.write(gpx_file.to_xml())
	    	r.close()
	    	
	    	rdp=open(pathGGA, "r")
	    	gpx_rdp = gpxpy.parse(rdp)
	    	segment1 = gpx_rdp.tracks[0].segments[0]
			coords = pd.DataFrame([
        	{'lat': p.latitude, 
        	'lon': p.longitude, 
         	'ele': p.elevation,
         	'time': p.time} for p in segment1.points])
			coords.set_index('time', drop=True, inplace=True)
			coords = coords[~coords.index.duplicated()]
			coords = coords.resample('1S').asfreq()
			rdp_coords = rdp(coords[['lon', 'lat']].values, epsilon=0.000007)
			
			value=int(0)
			rdp_coords = np.asarray(rdp_coords)
			for i in range(len(points)): 
  				if points[i].longitude == rdp_coords[value,0]:
        			rdp_coords[value,0] = points[i].longitude
        			rdp_coords[value,1] = points[i].latitude
        			value=value+int(1)
    		else:
        		points[i].latitude = "NaN"
        		points[i].longitude = "NaN"
        		points[i].elevation = "NaN"
        		
        	RDP_file = open (pathRDP, 'w')
			RDP_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n <gpx version=\"1.0\">\n \t<trk><name>Today</name><trkseg>\n \t</trkseg></trk>\n </gpx> \n")
			RDP_file.close()
			
			for i in range(len(points)): 
    			if points[i].longitude != "NaN":
        			RDP_file = open(pathRDP, 'r')
        			contents = RDP_file.readlines()
        			RDP_file.close()
        			contents.insert(lineinsert2, "\t\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{alt}</ele><time>{time}</time></trkpt>\n".format(lat=points[i].latitude,lon=points[i].longitude,alt=points[i].elevation, time=points[i].time))
        			RDP_file=open(pathRDP, 'w') 
        			contents = "".join(contents)
       				RDP_file.write(contents)
        			RDP_file.close()
	    	

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
from pykalman import KalmanFilter

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
pathKAL = os.path.join(folderpath,'track_raw_KAL.gpx')
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
lineinsert3=3

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
	    	
		#start of Point reduction 
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
	    	#end of point reduction
		
		#start of RDP smoothing
	    	rdp=open(pathGGA, "r")
	    	gpx_rdp = gpxpy.parse(rdp)
		#assign lat, long, ele values to array variable
	    	points1 = gpx_rdp.tracks[0].segments[0].points
			coords = pd.DataFrame([
        	{'lat': p.latitude, 
        	'lon': p.longitude, 
         	'ele': p.elevation,
         	'time': p.time} for p in points1])
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
		for i in range(len(points1)):
			#if the gpx coordinate is equal to the RDP residual value
  			if points1[i].longitude == rdp_coords[value,0]:
        			rdp_coords[value,0] = points1[i].longitude
        			rdp_coords[value,1] = points1[i].latitude
        			value=value+int(1)
    		else:
			#mask filtered RDP values to NaN
        		points1[i].latitude = "NaN"
        		points1[i].longitude = "NaN"
        		points1[i].elevation = "NaN"
        	
        	RDP_file = open (pathRDP, 'w')
		#write basic gpx header
		RDP_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n <gpx version=\"1.0\">\n \t<trk><name>Today</name><trkseg>\n \t</trkseg></trk>\n </gpx> \n")
		RDP_file.close()
		
		#for all elements in gpx file
		for i in range(len(points1)):
			#if long is not masked, e.g. NaN
    			if points1[i].longitude != "NaN":
        			RDP_file = open(pathRDP, 'r')
        			contents = RDP_file.readlines()
        			RDP_file.close()
				#insert value
        			contents.insert(lineinsert2, "\t\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{alt}</ele><time>{time}</time></trkpt>\n".format(lat=points1[i].latitude,lon=points1[i].longitude,alt=points1[i].elevation, time=points1[i].time))
        			RDP_file=open(pathRDP, 'w') 
        			contents = "".join(contents)
       				RDP_file.write(contents)
        			RDP_file.close()
				#else: all masked values won't be written
		#end of RDP algorithm
		
		#start of Kalman filter
		kal=open(pathGGA, "r")
	    	gpx_kal = gpxpy.parse(kal)
	    	points2 = gpx_kal.tracks[0].segments[0].points
		coords_kal = pd.DataFrame([
        		{'lat': p.latitude, 
        		'lon': p.longitude, 
         		'ele': p.elevation,
         		'time': p.time} for p in points2.points])
		coords_kal.set_index('time', drop=True, inplace=True)
		coords_kal = coords_kal[~coords_kal.index.duplicated()]
		coords_kal = coords_kal.resample('1S').asfreq()
    
		measurements = np.ma.masked_invalid(coords_kal[['lon', 'lat', 'ele']].values)
			
		F = np.array([[1, 0, 0, 1, 0, 0],
              		[0, 1, 0, 0, 1, 0],
              		[0, 0, 1, 0, 0, 1],
              		[0, 0, 0, 1, 0, 0],
              		[0, 0, 0, 0, 1, 0],
              		[0, 0, 0, 0, 0, 1]])

		H = np.array([[1, 0, 0, 0, 0, 0],
              		[0, 1, 0, 0, 0, 0],
              		[0, 0, 1, 0, 0, 0]])

		R = np.diag([1e-4, 1e-4, 100])**2

		initial_state_mean = np.hstack([measurements[0, :], 3*[0.]])
		initial_state_covariance = np.diag([1e-4, 1e-4, 50, 1e-6, 1e-6, 1e-6])**2

		kf = KalmanFilter(transition_matrices=F, 
                	observation_matrices=H, 
                 	observation_covariance=R,
                  	initial_state_mean=initial_state_mean,
                  	initial_state_covariance=initial_state_covariance,
                  	em_vars=['transition_covariance'])
			
		#computing the transition covariance takes a long time (~hrs)
		#kf = kf.em(measurements, n_iter=1000)
			
		#if the movement stays roughly the same, computing it once may be enough
		#therefore we use a pre-computed transition matrix (computed for the sample data)
		Q = np.array([[ 3.22502567e-09, -1.62005281e-09, -3.12598725e-07,
         			2.36235756e-09, -3.28570108e-09, -4.01744803e-07],
       				[ 1.62288350e-09,  3.22487582e-09,  2.32009027e-07,
         			3.28938075e-09,  2.36125951e-09,  9.62937862e-08],
       				[ 9.01612167e-09,  3.88914731e-07,  2.80701618e+01,
         			2.04054696e-07,  4.10267098e-07,  4.93801327e-01],
       				[ 3.07330494e-09, -9.48583279e-10, -2.63264766e-07,
         			5.62370096e-09, -5.49726348e-09, -7.36399308e-07],
       				[ 9.52392286e-10,  3.07293746e-09,  2.48317229e-07,
         			5.50374162e-09,  5.62174830e-09,  3.18959938e-07],
       				[-2.86837336e-08,  3.27220964e-07,  4.93804073e-01,
         			3.03007065e-07,  7.43677546e-07,  2.42493005e-02]])
         	Q = 0.5*(Q + Q.T) # assure symmetry
		kf.transition_covariance = Q
         					
         	#we smooth the data 
         	state_means, state_vars = kf.smooth(measurements)
		
		#we write the basic gpx header
		KAL_file = open (pathKAL, 'w')
		KAL_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n <gpx version=\"1.0\">\n \t<trk><name>Today</name><trkseg>\n \t</trkseg></trk>\n </gpx> \n")
		KAL_file.close()
		
		#we replace all gpx values with the newly computed means
		state_means = np.asarray(state_means)
		for i in range(len(points2)): 
    			state_means[i,0] = points2[i].longitude
    			state_means[i,1] = points2[i].latitude

		#for all elements in gpx file
		for i in range(len(points1)):
        		RDP_file = open(pathRDP, 'r')
        		contents = RDP_file.readlines()
        		RDP_file.close()
			#insert value
        		contents.insert(lineinsert3, "\t\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{alt}</ele><time>{time}</time></trkpt>\n".format(lat=points2[i].latitude,lon=points2[i].longitude,alt=points2[i].elevation, time=points2[i].time))
        		RDP_file=open(pathRDP, 'w') 
        		contents = "".join(contents)
       			RDP_file.write(contents)
        		RDP_file.close()
			lineinsert3=lineinsert3+1
		#end of Kalman
		
	    	

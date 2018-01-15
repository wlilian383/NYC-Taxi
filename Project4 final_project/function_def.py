import csv
import sys
import time
import copy
from datetime import datetime
import matplotlib.pyplot as plt
from math import sin, asin, cos, radians, fabs, sqrt , ceil, floor
import numpy as np

def readfile(filename) :
	inputFile1 = str(filename)
	dataReadIn1 = []
	with open (inputFile1, 'r') as f :
		for line in f :
			dataReadIn1.append ([row for row in line.strip().split(',')])
	f.close ()
	return dataReadIn1

def writefile(list_input,filename2):
	fw = open (filename2, 'w') 
	for cnt1 in range( len(list_input) ) :  
		for cnt2 in range( len(list_input[0])-1 ):
			fw.write("%s," % list_input[cnt1][cnt2])
		fw.write("%s\n" % list_input[cnt1][len(list_input[0])-1] )

def computeTimeError( pickTime, dropTime, trip_duration ):
	try:
		pickTime = datetime.strptime(pickTime,'%Y/%m/%d %H:%M')
		dropTime = datetime.strptime(dropTime,'%Y/%m/%d %H:%M')
	except ValueError:
		pickTime = datetime.strptime(pickTime,'%Y-%m-%d %H:%M:%S')
		dropTime = datetime.strptime(dropTime,'%Y-%m-%d %H:%M:%S')
	datatime_duration = dropTime - pickTime
	#print(datatime_duration)
	# split the day and time (ex: 40 days, 19:32:00 => 40 and 19:32:00)
	datatimeList = str(datatime_duration).split(' days, ')# ##
	if len(datatimeList) == 2:
		days = int(datatimeList[0])
		times = datatimeList[1]
	else:
		days = 0
		times = datatimeList[0]
	#print( str(days) + " "   + times )
	hours, minutes, seconds = map(int ,times.split(':'))
	datatime_duration = ((days*24) + hours) * 3600 + minutes * 60

	#compute the time error
	time_error = abs(trip_duration - datatime_duration)
	
	return time_error

def computeDatetime( Time ):
	try:
		dt = datetime.strptime(Time,'%Y/%m/%d %H:%M')
	except ValueError:
		dt = datetime.strptime(Time,'%Y-%m-%d %H:%M:%S')
	return dt

def hav( theta ):  
	s = sin( theta / 2 )  
	return s * s    

def get_distance_hav( lat0, lng0, lat1, lng1 ):  
	# 地球平均半徑，6371km  
	EARTH_RADIUS = 6371           
	
	# 用haversine公式算球面的距
	# 經緯度轉換成弧度
	lat0 = radians(lat0)  
	lat1 = radians(lat1)  
	lng0 = radians(lng0)  
	lng1 = radians(lng1)  
   
	dlng = fabs(lng0 - lng1)  
	dlat = fabs(lat0 - lat1)  
	h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)  
	distance = 2 * EARTH_RADIUS * asin(sqrt(h))  
   
	return distance 
	
def computeSpeed( lat0, lng0, lat1, lng1, trip_duration):  
	dist = get_distance_hav( lat0, lng0, lat1, lng1 )
	time = trip_duration / 3600
	velocity = dist / time
	return velocity

def getCloumnByName( columnName, columnNameList ):
	index = columnNameList.index(columnName)
	return index

def Plot( a ):
	time=[]
	speed=[]
	dist=[]
	passenger_count=[]
	pickup_datetime=[]
	
	peak_speed=[]
	nonpeak_speed=[]
	
	monday=[0 for i in range(0,24)]
	tuesday=[0 for i in range(0,24)]
	wednesday=[0 for i in range(0,24)]
	thursday=[0 for i in range(0,24)]
	friday=[0 for i in range(0,24)]
	saturday=[0 for i in range(0,24)]
	sunday=[0 for i in range(0,24)]
	counter=[[0 for i in range(0,24)] for i in range(0,7)]
	
	for cnt in range(1,len(a)):
		#time.append( int(a[cnt][getCloumnByName('trip_duration',a[0])]) )
		#dist.append( float(a[cnt][getCloumnByName('distance',a[0])]) )
		#speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
		#passenger_count.append( int(a[cnt][getCloumnByName('passenger_count',a[0])]) )
		pickup_datetime.append( a[cnt][getCloumnByName('pickup_datetime',a[0])] )
		
		PickUpDateTime = computeDatetime(a[cnt][getCloumnByName('pickup_datetime',a[0])])
		'''if(PickUpDateTime.weekday() != 5 or PickUpDateTime.weekday() != 6 and PickUpDateTime.weekday() != 7 ):
			if(PickUpDateTime.hour == 7 or PickUpDateTime.hour == 8 or PickUpDateTime.hour == 9 or PickUpDateTime.hour == 18
			or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 20):
				peak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
			else:
				nonpeak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
		
		elif( PickUpDateTime.weekday() == 5 ):
			if(PickUpDateTime.hour == 7 or PickUpDateTime.hour == 8 or PickUpDateTime.hour == 9 or PickUpDateTime.hour == 18
			or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 20 or PickUpDateTime.hour == 22 or PickUpDateTime.hour == 23):
				peak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
			else:
				nonpeak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
				
		elif( PickUpDateTime.weekday() == 6 ):
			if(PickUpDateTime.hour == 18 or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 20 or PickUpDateTime.hour == 22
			or PickUpDateTime.hour == 23 or PickUpDateTime.hour == 0 or PickUpDateTime.hour == 1 ):
				peak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
			else:
				nonpeak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )

		else:
			if(PickUpDateTime.hour == 17 or PickUpDateTime.hour == 18 or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 0
			or PickUpDateTime.hour == 1 ):
				peak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )
			else:
				nonpeak_speed.append( float(a[cnt][getCloumnByName('speed',a[0])]) )'''
		if(PickUpDateTime.weekday() == 1):
			monday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[0][PickUpDateTime.hour]+=1
		elif(PickUpDateTime.weekday() == 2):
			tuesday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[1][PickUpDateTime.hour]+=1
		elif(PickUpDateTime.weekday() == 3):
			wednesday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[2][PickUpDateTime.hour]+=1
		elif(PickUpDateTime.weekday() == 4):
			thursday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[3][PickUpDateTime.hour]+=1
		elif(PickUpDateTime.weekday() == 5):
			friday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[4][PickUpDateTime.hour]+=1
		elif(PickUpDateTime.weekday() == 6):
			saturday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[5][PickUpDateTime.hour]+=1
		else:
			sunday[PickUpDateTime.hour]+= float(a[cnt][getCloumnByName('speed',a[0])])
			counter[6][PickUpDateTime.hour]+=1
	for cnt in range(0,24):
		print(str(monday[cnt]/counter[0][cnt]),end=',')
	print('\n')
	for cnt in range(0,24):
		print(str(tuesday[cnt]/counter[0][cnt]),end=',')
	print('\n')
	for cnt in range(0,24):
		print(str(wednesday[cnt]/counter[0][cnt]),end=',')
	print('\n')
	for cnt in range(0,24):
		print(str(thursday[cnt]/counter[0][cnt]),end=',')
	print('\n')
	for cnt in range(0,24):
		print(str(friday[cnt]/counter[0][cnt]),end=',')
	print('\n')
	for cnt in range(0,24):
		print(str(saturday[cnt]/counter[0][cnt]),end=',')
	print('\n')
	for cnt in range(0,24):
		print(str(sunday[cnt]/counter[0][cnt]),end=',')
	
	#plt.title('Scatter Time-Distance')  
	#plt.xlabel('time')
	#plt.ylabel('dist')  
	#plt.scatter(time,dist)
	
	#plt.title(Scatter Speed-Distance')
	#plt.xlabel('speed')
	#plt.ylabel('dist')
	#plt.scatter(speed,dist)
	
	#f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
	#ax1.scatter(peak_pickup,peak_speed,c = 'r')
	#ax1.set_title('Pick Up Time vs. Speed')
	#ax2.scatter(nonpeak_pickup,nonpeak_speed,c = 'b')
	
	#print("Rush-hour-avg-speed:", np.mean(peak_speed))
	#print("Non-rush-hour-avg-speed:", np.mean(nonpeak_speed))
	#bins = np.linspace(0, 50, 50)
	#plt.subplot(211)
	#plt.hist(np.array(peak_speed),bins=bins)
	#plt.title('Rush-hour Speed vs. Non-rush-hour Speed')
	#plt.subplot(212)
	#plt.hist(np.array(nonpeak_speed),bins=bins,color='r')
		
	plt.show()
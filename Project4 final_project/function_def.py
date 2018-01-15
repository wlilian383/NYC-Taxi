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
	datatime_duration = computeDatetime(dropTime) - computeDatetime(pickTime)
	
	# split the day and time (ex: 40 days, 19:32:00 => 40 and 19:32:00)
	datatimeList = []
	if str(datatime_duration).find(' days, ')!=-1 :
		datatimeList = str(datatime_duration).split(' days, ')
	elif str(datatime_duration).find(' day, ')!=-1 :
		datatimeList = str(datatime_duration).split(' day, ')
	else:
		datatimeList.append(datatime_duration)

	# check the datatime formate (if len is two, means format is day + time, other means only times)
	if len(datatimeList) == 2:
		days = int(datatimeList[0])
		times = datatimeList[1]
	else:
		days = 0
		times = datatimeList[0]
	
	hours, minutes, seconds = map(int ,str(times).split(':'))
	datatime_duration = ((days*24) + hours) * 3600 + minutes * 60

	#compute the time error
	time_error = abs(trip_duration - datatime_duration)
	return time_error

def computeDatetime( Time ):
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

def getColByName( columnName, columnNameList ):
	index = columnNameList.index(columnName)
	return index

def roundTripAirport( lat0, lng0, lat1, lng1 ):# 這邊應該要放 經 緯 經 緯(而不是上面打的那樣)
	
	#JFK / LGA
	airportList = [[4.5,-73.7822222222,40.6441666667],[4.5,-73.87396590000003,40.7769271]]
	airportFlag = []
	for airport in airportList:
		r = airport[0]
		airport_lat = airport[1]
		airport_lng = airport[2]
		pickup_dis = get_distance_hav(airport_lat, airport_lng, lat0, lng0)
		dropup_dis = get_distance_hav(airport_lat,airport_lng, lat1, lng1)

		if pickup_dis < r and dropup_dis < r: # "interTrip_in_airport"
			airportFlag.append(3)
		elif pickup_dis < r: # "pickup_in_airport"
			airportFlag.append(1)
		elif dropup_dis < r: # "dropoff_in_airport"
			airportFlag.append(2)
		else: #"no"
			airportFlag.append(0)

	if airportFlag[0]!=0 and airportFlag[1]!=0:
		airport = "interTrip_between_two_airport"
	elif airportFlag[0]==1 or airportFlag[1]==1:
	 	airport = "pickup_in_an_airport"
	elif airportFlag[0]==2 or airportFlag[1]==2:
		airport = "dropoff_in_an_airport"
	elif airportFlag[0]==3 or airportFlag[1]==3:
		airport = "interTrip_in_an_airport"
	else:
		airport = "in_downtown"
	return airport

def checkPlaceNYC( long, lat ):
	if ( lat > 40.566874 and lat < 40.916477 and long > -74.041532 and long < -73.728422 ):
		return 1
	elif ( lat > 40.502164 and lat < 40.648196 and long > -74.253019 and long < -74.051145):
		return 1
	else:
		return 0

def PlotScatterTimeDistance( a ):
	time=[]
	dist=[]
	for cnt in range(1,len(a)):
		time.append( int(a[cnt][getColByName('trip_duration',a[0])]) )
		dist.append( float(a[cnt][getColByName('distance',a[0])]) )
	plt.title('Scatter Time-Distance')  
	plt.xlabel('time')
	plt.ylabel('dist')  
	plt.scatter(time,dist)
	plt.show()

def PlotScatterSpeedDistance( a ):
	speed=[]
	dist=[]
	for cnt in range(1,len(a)):
		dist.append( float(a[cnt][getColByName('distance',a[0])]) )
		speed.append( float(a[cnt][getColByName('speed',a[0])]) )
	plt.title('Scatter Speed-Distance')
	plt.xlabel('speed')
	plt.ylabel('dist')
	plt.scatter(speed,dist)
	plt.show()

def RushHourAndNonRushHourSpeedHist( a ):
	peak_speed=[]
	nonpeak_speed=[]
	pickup_datetime=[]
	for cnt in range(1,len(a)):
		pickup_datetime.append( a[cnt][getColByName('pickup_datetime',a[0])] )
		# convert to datetime format
		PickUpDateTime = computeDatetime(a[cnt][getColByName('pickup_datetime',a[0])])
		if( RushHour(PickUpDateTime) == 1 ):
			peak_speed.append( float(a[cnt][getColByName('speed',a[0])]) )
		else:
			nonpeak_speed.append( float(a[cnt][getColByName('speed',a[0])]) )
	
	print("Rush-hour-avg-speed:", np.mean(peak_speed))
	print("Non-rush-hour-avg-speed:", np.mean(nonpeak_speed))
	bins = np.linspace(0, 50, 50)
	plt.subplot(211)
	plt.hist(np.array(peak_speed),bins=bins,color='r')
	plt.title('Rush-hour Speed vs. Non-rush-hour Speed')
	plt.subplot(212)
	plt.hist(np.array(nonpeak_speed),bins=bins)
	plt.show()

def PlotScatterTimeGuess( a ):
	time=[]
	guess=[]
	for cnt in range(1,len(a)):
		time.append( int(a[cnt][getColByName('trip_duration',a[0])]) )
		guess.append( float(a[cnt][getColByName('guesstime',a[0])]) ) #may have problem because the weekday format ',' is the saparator of csv file
	plt.title('Scatter Time-Guesstime')  
	plt.xlabel('time')
	plt.ylabel('guesstime')  
	plt.scatter(time,guess)
	plt.show()

def RushHour( PickUpDateTime ):
	if(PickUpDateTime.weekday() != 4 or PickUpDateTime.weekday() != 5 and PickUpDateTime.weekday() != 6 ):
		if(PickUpDateTime.hour == 7 or PickUpDateTime.hour == 8 or PickUpDateTime.hour == 9 or PickUpDateTime.hour == 18
		or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 20):
			return 1
		else:
			return 0
	elif( PickUpDateTime.weekday() == 4 ):
		if(PickUpDateTime.hour == 7 or PickUpDateTime.hour == 8 or PickUpDateTime.hour == 9 or PickUpDateTime.hour == 18
		or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 20 or PickUpDateTime.hour == 22 or PickUpDateTime.hour == 23):
			return 1
		else:
			return 0
	elif( PickUpDateTime.weekday() == 5 ):
		if(PickUpDateTime.hour == 18 or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 20 or PickUpDateTime.hour == 22
		or PickUpDateTime.hour == 23 or PickUpDateTime.hour == 0 or PickUpDateTime.hour == 1 ):
			return 1
		else:
			return 0
	else:
		if(PickUpDateTime.hour == 17 or PickUpDateTime.hour == 18 or PickUpDateTime.hour == 19 or PickUpDateTime.hour == 0
		or PickUpDateTime.hour == 1 ):
			return 1
		else:
			return 0
	
def CountSpeedOfEachDayAndHour( a ):
	# speed of each day and hour
	speed=[[0.0 for i in range(0,24)] for i in range(0,7)]
	# event number of each day and hour
	counter=[[0 for i in range(0,24)] for i in range(0,7)]
	returnlist=[[0.0 for i in range(0,24)] for i in range(0,7)]
	
	for cnt in range(1,len(a)):
		# convert to datetime format
		PickUpDateTime = computeDatetime(a[cnt][getColByName('pickup_datetime',a[0])])
		
		speed[PickUpDateTime.weekday()][PickUpDateTime.hour]+= float(a[cnt][getColByName('speed',a[0])])
		counter[PickUpDateTime.weekday()][PickUpDateTime.hour]+=1

	# print average speed of each day and hour
	for day in range(0,7):
		for hour in range(0,24):
			returnlist[day][hour]=(speed[day][hour]/counter[day][hour])
	print(returnlist)
	return returnlist
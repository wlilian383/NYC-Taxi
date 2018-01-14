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
		pickTime = datetime.strptime(pickTime,'%Y/%m/%d %H:%M:%S')
		dropTime = datetime.strptime(dropTime,'%Y/%m/%d %H:%M:%S')
	except ValueError:
		pickTime = datetime.strptime(pickTime,'%Y-%m-%d %H:%M:%S')
		dropTime = datetime.strptime(dropTime,'%Y-%m-%d %H:%M:%S')
	datatime_duration = dropTime - pickTime
	
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
	try:
		dt = datetime.strptime(Time,'%Y/%m/%d %H:%M:%S')
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

def roundTripAirport( lat0, lng0, lat1, lng1 ):
	r = 8
	airport_lat = -73.7822222222
	airport_lng = 40.6441666667
	pickup_dis = get_distance_hav(airport_lat, airport_lng, lat0, lng0)
	dropup_dis = get_distance_hav(airport_lat,airport_lng, lat1, lng1)

	if pickup_dis < r and dropup_dis < r:
		airport = "interTrip_in_airport"
	elif pickup_dis < r:
		airport = "pickup_in_airport"
	elif dropup_dis < r:
		airport = "dropoff_in_airport"
	else:
		airport = "no"
	return airport

def getCloumnByName( columnName, columnNameList ):
	index = columnNameList.index(columnName)
	return index

if __name__ == "__main__" :
	# timer start
	tStart = time.time()

	# check usage for this program
	if len(sys.argv) != 2:
		print("Usage error!")
		sys.exit()

	# input file name and output file name
	input_fileName = sys.argv[1]   #./data/train.csv
	output_fileName = "./data/testoutput.csv"
	
	# read the datas
	inputList = readfile( input_fileName )

	# add new empty columns
	inputList[0].append('time_error')
	inputList[0].append('distance')
	inputList[0].append('speed')
	inputList[0].append('airport')
	
	# fill the value of new columns
	for row in inputList[1:]:
		trip_duration = int(row[ getCloumnByName('trip_duration',inputList[0]) ])
		pickup_datetime = row[ getCloumnByName('pickup_datetime',inputList[0]) ]
		dropoff_datetime = row[ getCloumnByName('dropoff_datetime',inputList[0]) ]
		pickup_longitude = float(row[ getCloumnByName('pickup_longitude',inputList[0]) ])
		pickup_latitude = float(row[ getCloumnByName('pickup_latitude',inputList[0]) ])
		dropoff_longitude = float(row[ getCloumnByName('dropoff_longitude',inputList[0]) ])
		dropoff_latitude = float(row[ getCloumnByName('dropoff_latitude',inputList[0]) ])
		
		time_error = computeTimeError( pickup_datetime, dropoff_datetime, trip_duration )
		distance =  get_distance_hav( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude )
		speed = computeSpeed( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, trip_duration )
		airport = roundTripAirport( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude )
		row.append(time_error)
		row.append(distance)
		row.append(speed)
		row.append(airport)
	print("Number of datas (Original) : " + str(len(inputList)-1) )
	
	# filter the outliers with trip_duration and distance
	for row in inputList[1:]:
		trip_duration = int(row[ getCloumnByName('trip_duration',inputList[0]) ])
		distance = float(row[ getCloumnByName('distance',inputList[0]) ])
		speed = float(row[ getCloumnByName('speed',inputList[0]) ])
		
		if distance > 100:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
		elif trip_duration > 9000 or trip_duration < 60:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
		elif speed > 200:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
	print("Number of datas (After) : " + str(len(inputList)-1))
	
	writefile( inputList, "train_deleteOutlier.csv")

	#writefile( inputList, "train_newColumn.csv")
	# timer end
	tEnd = time.time()

	# print execution time
	print("Execution time: ", tEnd - tStart)
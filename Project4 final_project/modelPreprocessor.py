import sys
sys.path.append("./")
from function_def import *
from evalution import *
if __name__ == "__main__" :
	# timer start
	tStart = time.time()

	# check usage for this program
	if len(sys.argv) != 2:
		print("Usage error!")
		sys.exit()

	# input file name and output file name
	input_fileName = sys.argv[1]   #train_deleteOutlier.csv
	output_fileName = "model.csv"
	
	# read the datas
	inputList = readfile( input_fileName )

	# add new empty columns
	inputList[0].append('airport_indicator')
	inputList[0].append('rushhour')
	inputList[0].append('guesstime')
	#inputList[0].append('weekday')
	
	avg_speed_of_all = CountSpeedOfEachDayAndHour( inputList )
	
	avg_speed_of_airport = [0,0,0,0]
	n_list = [0,0,0,0]
	for row in inputList[1:]:
		pickup_longitude = float(row[ getColByName('pickup_longitude',inputList[0]) ])
		pickup_latitude = float(row[ getColByName('pickup_latitude',inputList[0]) ])
		dropoff_longitude = float(row[ getColByName('dropoff_longitude',inputList[0]) ])
		dropoff_latitude = float(row[ getColByName('dropoff_latitude',inputList[0]) ])
		PickUpDateTime = computeDatetime(row[ getColByName('pickup_datetime',inputList[0]) ])
		distance = float(row[ getColByName('distance',inputList[0]) ])
		airport= str(roundTripAirport( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude) )
		if airport == "interTrip_between_two_airport":
			avg_speed_of_airport[0] += float(row[ getColByName('speed',inputList[0]) ])
			n_list[0] += 1
		elif airport == "pickup_in_an_airport":
			avg_speed_of_airport[1] += float(row[ getColByName('speed',inputList[0]) ])
			n_list[1] += 1
		elif airport == "dropoff_in_an_airport":
			avg_speed_of_airport[2] += float(row[ getColByName('speed',inputList[0]) ])
			n_list[2] += 1
		elif airport == "interTrip_in_an_airport":
			avg_speed_of_airport[3] += float(row[ getColByName('speed',inputList[0]) ])
			n_list[3] += 1
	for i in range(4):
		avg_speed_of_airport[i] = avg_speed_of_airport[i]/n_list[i]

	# fill the value of new columns
	for row in inputList[1:]:
		weekday = [0 for i in range(0,7)]
		rushhour = 0
		airport_indicator = 0
		
		pickup_longitude = float(row[ getColByName('pickup_longitude',inputList[0]) ])
		pickup_latitude = float(row[ getColByName('pickup_latitude',inputList[0]) ])
		dropoff_longitude = float(row[ getColByName('dropoff_longitude',inputList[0]) ])
		dropoff_latitude = float(row[ getColByName('dropoff_latitude',inputList[0]) ])
		PickUpDateTime = computeDatetime(row[ getColByName('pickup_datetime',inputList[0]) ])
		distance = float(row[ getColByName('distance',inputList[0]) ])
		

		#if(str(roundTripAirport( pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude) ) != "in_downtown"):
		if(str(roundTripAirport( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude) ) != "in_downtown"):
			airport_indicator = 1
		
		weekday[PickUpDateTime.weekday()] = 1
		
		if( RushHour(PickUpDateTime) == 1 ):
			rushhour = 1

		airport= str(roundTripAirport( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude) )
		"""
		if airport == "interTrip_between_two_airport":
			guesstime = distance/avg_speed_of_airport[0] *3600
		elif airport == "pickup_in_an_airport":
			guesstime = distance/avg_speed_of_airport[1] *3600
		elif airport == "dropoff_in_an_airport":
			guesstime = distance/avg_speed_of_airport[2] *3600
		elif airport == "interTrip_in_an_airport":
			guesstime = distance/avg_speed_of_airport[3] *3600
		else:
			guesstime = (distance/float(avg_speed_of_all[PickUpDateTime.weekday()-1][PickUpDateTime.hour]))*3600
		"""
		guesstime = (distance/float(avg_speed_of_all[PickUpDateTime.weekday()-1][PickUpDateTime.hour]))*3600
		row.append(airport_indicator)
		row.append(rushhour)
		row.append(guesstime)
		#row.append(weekday)

	writefile( inputList, output_fileName )

	# timer end
	tEnd = time.time()

	# print execution time
	print("Execution time: ", tEnd - tStart)

	print("\n\n")
	evalutaion(output_fileName)

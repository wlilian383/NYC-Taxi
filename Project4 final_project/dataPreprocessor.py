import sys
sys.path.append("./")
from function_def import *

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
		trip_duration = int(row[ getColByName('trip_duration',inputList[0]) ])
		pickup_datetime = row[ getColByName('pickup_datetime',inputList[0]) ]
		dropoff_datetime = row[ getColByName('dropoff_datetime',inputList[0]) ]
		pickup_longitude = float(row[ getColByName('pickup_longitude',inputList[0]) ])
		pickup_latitude = float(row[ getColByName('pickup_latitude',inputList[0]) ])
		dropoff_longitude = float(row[ getColByName('dropoff_longitude',inputList[0]) ])
		dropoff_latitude = float(row[ getColByName('dropoff_latitude',inputList[0]) ])
		
		time_error = computeTimeError( pickup_datetime, dropoff_datetime, trip_duration )
		distance =  get_distance_hav( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude )
		speed = computeSpeed( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, trip_duration )
		airport = roundTripAirport( pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude )
		row.append(time_error)
		row.append(distance)
		row.append(speed)
		row.append(airport)
	#print("Number of datas (Original) : " + str(len(inputList)-1) ) # 1458644
	
	# filter the outliers with longitude, latitude, distance, trip_duration and speed
	#for row in inputList[1:]:
		trip_duration = int(row[ getColByName('trip_duration',inputList[0]) ])
		distance = float(row[ getColByName('distance',inputList[0]) ])
		speed = float(row[ getColByName('speed',inputList[0]) ])
		if checkPlaceNYC( pickup_longitude, pickup_latitude ) == 0:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
		elif checkPlaceNYC( dropoff_longitude, dropoff_latitude ) == 0:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
		elif distance > 100:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
		elif trip_duration > 9000 or trip_duration < 60:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
		elif speed > 200:
			rowIndex = inputList.index(row)
			del inputList[rowIndex]
	print("Number of datas (After) : " + str(len(inputList)-1))

	cnt = [0.0,0.0,0.0,0.0]
	for row in inputList[1:]:
		airport = row[ getColByName('airport',inputList[0]) ]
		if airport == "interTrip_between_two_airport":
			cnt[0] +=1 
		elif airport == "pickup_in_an_airport":
	 		cnt[1] +=1
		elif airport == "dropoff_in_an_airport":
			cnt[2] +=1
		elif airport == "interTrip_in_an_airport":
			cnt[3] +=1

	cnt_sum = 0.0
	for cnt_each in cnt:
		cnt_sum += cnt_each
	print("---------- Around airport data: " + str(cnt_sum) + "(" + str(cnt_sum/(len(inputList)-1)) + ") ----------")
	print("InterTrip_between_two_airport: " + str(cnt[0]) + " (" + str(cnt[0]/cnt_sum*100) + "%)" )
	print("Pickup_in_an_airport: " + str(cnt[1]) + " (" + str(cnt[1]/cnt_sum*100) + "%)" )
	print("Dropoff_in_an_airport: " + str(cnt[2]) + " (" + str(cnt[2]/cnt_sum*100) + "%)" )
	print("InterTrip_in_an_airport: " + str(cnt[3]) + " (" + str(cnt[3]/cnt_sum*100) + "%)" )

	writefile( inputList, "train_deleteOutlier.csv")

	#writefile( inputList, "train_newColumn.csv")
	# timer end
	tEnd = time.time()

	# print execution time
	print("Execution time: ", tEnd - tStart)
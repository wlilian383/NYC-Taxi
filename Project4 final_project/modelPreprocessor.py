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
	input_fileName = sys.argv[1]   #train_deleteOutlier.csv
	output_fileName = "model.csv"
	
	# read the datas
	inputList = readfile( input_fileName )

	# add new empty columns
	inputList[0].append('airport_indicator')
	inputList[0].append('rushhour')
	inputList[0].append('guesstime')
	inputList[0].append('weekday')
	
	avg_speed_of_all = [[16.5364754,17.2160745,17.2594283,17.98241077,21.20441525,20.97274278,15.56577927,11.36656457,8.953167491,8.610826476,8.623342556,8.5922236,8.77922379,8.970203423,9.005992647,8.905255424,9.45198565,9.239495406,9.380169564,10.76366786,12.05836378,12.40554834,12.86069166,14.30677838],
	[18.00330679,19.62520172,20.91237372,22.55554687,22.85064967,19.75957496,16.17983866,11.70393332,9.303383749,8.64818806,8.945362116,8.595102549,8.995294289,8.971067797,8.812355907,8.558920471,9.090270913,8.774407165,8.813175484,10.60189026,12.1681334,12.81569537,13.26016697,15.11602736],
	[20.55358936,22.41257168,23.54597015,27.24688047,24.99851343,21.26957928,16.71067961,11.72961968,9.179686232,8.676261866,9.169486401,8.772132003,9.192811508,9.363316407,9.217871113,8.958935034,9.036257745,8.666585232,9.097459433,10.79759833,11.99074745,12.87624541,13.50517617,17.16798264],
	[26.32780732,32.84932971,39.09962884,47.10768802,38.22620303,24.09811545,15.53353967,11.30183917,9.306781849,8.643138933,9.201916445,9.01668825,9.769285807,10.19440071,9.850372209,9.187748118,9.413982185,9.462076105,9.434023954,10.77016572,11.16352235,11.18334637,12.84954821,17.35527165],
	[31.09961858,49.4437893,73.29566109,86.54441899,54.99072219,19.4026113,8.88165604,6.358735726,6.979016026,9.37994609,12.03841174,11.76157363,12.28651216,12.01343197,10.85261454,11.12450552,11.57550938,10.37569667,9.336124132,9.523295877,9.124945089,9.663632319,11.50079953,16.87466904],
	[32.12381846,52.73707669,76.11932585,97.0564736,62.76699507,18.56190555,8.150733508,5.560840668,6.221834269,8.627394755,12.52747096,12.87834344,12.84730567,12.41982966,11.5280143,11.4751,12.56600642,11.14700612,9.372881735,9.354139487,9.392593177,9.639639515,10.36995485,12.12849],
	[17.22619307,17.82360247,19.00408943,21.77062729,26.13012598,21.93470461,15.4673505,10.66591044,9.047441778,8.977712185,9.233097777,9.248718271,9.433182105,9.774605861,9.834280157,10.1050188,10.80030008,10.05306013,9.996190209,10.96216351,11.7634136,11.86554544,11.60109964,12.50492135]]

	
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
		
		guesstime = (distance/float(avg_speed_of_all[PickUpDateTime.weekday()-1][PickUpDateTime.hour]))*3600
		
		row.append(airport_indicator)
		row.append(rushhour)
		row.append(guesstime)
		row.append(weekday)

	writefile( inputList, output_fileName )

	# timer end
	tEnd = time.time()

	# print execution time
	print("Execution time: ", tEnd - tStart)
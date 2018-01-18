from function_def import *
import copy
from evalution import *

def readDf( fileName ):
	with open( fileName , 'r') as reader:
		df = pd.read_csv( fileName , delimiter = ',')
		return df
if __name__ == "__main__" :
	# timer start
	tStart = time.time()
	df = readDf("train_deleteOutlier_old.csv")
	#df = readDf( sys.argv[1] )
	n = len(df)

	
	cnt_max = 0
	
	# count max of peo_cnt
	for i in range(n):
		peo_cnt = int(df['passenger_count'][i])
		if peo_cnt > cnt_max:
			cnt_max = peo_cnt

	modelList = []
	n_list = []
	modelList = []
	n_list = []
	for cnt in range(5):
		modelList.append([])
		n_list.append([])
		for i in range(cnt_max+1):
			modelList[cnt].append([])
			n_list[cnt].append([])
			for j in range(7):
				modelList[cnt][i].append([])
				n_list[cnt][i].append([])
				for k in range(24):
					modelList[cnt][i][j].append(0)
					n_list[cnt][i][j].append(0)
	for cnt in range(n):
		try:
			dt = datetime.strptime(df['pickup_datetime'][cnt],'%Y/%m/%d %H:%M')
		except ValueError:
			dt = datetime.strptime(df['pickup_datetime'][cnt],'%Y-%m-%d %H:%M:%S')

		weekday = int(dt.weekday())

		times = dt.time()
		hours, minutes, seconds = map(int ,str(times).split(':'))
		hours = int(hours)

		peo_cnt = int(df['passenger_count'][cnt]) 
		speed = int(df['speed'][cnt])
		airport = df['airport'][cnt]
		case = -1
		if airport == "in_downtown":
			case = 0
		elif airport == "interTrip_between_two_airport":
			case = 1	
		elif airport == "pickup_in_an_airport":
			case = 2
		elif airport == "dropoff_in_an_airport":
			case = 3		
		elif airport == "interTrip_in_an_airport":
			case = 4

		modelList[case][peo_cnt][weekday][hours] += speed
		n_list[case][peo_cnt][weekday][hours]+= 1

	for cnt1 in range(5):
		for cnt2 in range(cnt_max+1):
			for cnt3 in range(7):
				for cnt4 in range(24):
					if n_list[cnt1][cnt2][cnt3][cnt4]!=0:
						modelList[cnt1][cnt2][cnt3][cnt4] = modelList[cnt1][cnt2][cnt3][cnt4]/n_list[cnt1][cnt2][cnt3][cnt4]
	
	df2 = readDf("train_deleteOutlier.csv")

	df2['guesstime']=""
	for cnt in range(n):
		if cnt % 100 == 0:
			print("The number of loop: " + str(cnt))
		try:
			dt = datetime.strptime(df2['pickup_datetime'][cnt],'%Y/%m/%d %H:%M')
		except ValueError:
			dt = datetime.strptime(df2['pickup_datetime'][cnt],'%Y-%m-%d %H:%M:%S')

		weekday = int(dt.weekday())

		times = dt.time()
		hours, minutes, seconds = map(int ,str(times).split(':'))
		hours = int(hours)

		peo_cnt = int(df2['passenger_count'][cnt]) 
		distance = df2['distance'][cnt]
		airport = df2['airport'][cnt]

		if airport == "in_downtown":
			case = 0
		elif airport == "interTrip_between_two_airport":
			case = 1	
		elif airport == "pickup_in_an_airport":
			case = 2
		elif airport == "dropoff_in_an_airport":
			case = 3		
		elif airport == "interTrip_in_an_airport":
			case = 4
		speed = modelList[case][peo_cnt][weekday][hours]
		if speed !=0:
			guesstime = (distance / speed)*3600
		df2['guesstime'][cnt] = guesstime
	
	df2.to_csv("new_output2.csv")
	# timer end
	tEnd = time.time()
		
	# print execution time
	print("Execution time: ", tEnd - tStart)


	#print("\n\n")
	#evalutaion("new_output.csv")
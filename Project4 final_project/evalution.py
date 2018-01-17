from function_def import *
import math
import pandas as pd

if __name__ == "__main__" :
	if len(sys.argv)!=2:
		print("Useage error: [evalutaion output]")
		sys.exit()

	# timer start
	tStart = time.time()

	df = readDf( sys.argv[1] )
	errorSum = 0.0
	RSMLE = 0.0
	n = len(df)
	for i in range(n):
		actual = float(df['trip_duration'][i])
		predict = float(df['guesstime'][i])
		error = abs( actual - predict )
		RSMLE_each = (math.log(predict+1) - math.log(actual+1))**2
		errorSum += error
		RSMLE += RSMLE_each

	RSMLE = sqrt(RSMLE/n)
	# timer end
	tEnd = time.time()
	print("Average time error: " + str(errorSum/n) )
	print("RSMLE: " + str(RSMLE) )

	print("Execution time: ", tEnd - tStart)
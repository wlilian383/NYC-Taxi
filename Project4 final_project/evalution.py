from function_def import *
import pandas as pd

def readDf( fileName ):
	with open( fileName , 'r') as reader:
		df = pd.read_csv( fileName , delimiter = ',')
		return df


if __name__ == "__main__" :
	if len(sys.argv)!=2:
		print("Useage error: [evalutaion output]")
		sys.exit()


	# timer start
	tStart = time.time()

	df = readDf( sys.argv[1] )
	errorSum = 0.0
	for i in range(len(df)):
		error = abs( float(df['trip_duration'][i]) - float(df['guesstime'][i]) )
		errorSum += error

	# timer end
	tEnd = time.time()
	print("Average time error: " + str(errorSum/len(df)) )
	print("Execution time: ", tEnd - tStart)
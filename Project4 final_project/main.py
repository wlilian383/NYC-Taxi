import sys
sys.path.append("./")
from function_def import *

def main():
	# timer start
	tStart = time.time()
	
	#a = readfile( "train_deleteOutlier.csv" )
	
	#PlotScatterTimeDistance( a )
	#PlotScatterSpeedDistance( a )
	#RushHourAndNonRushHourSpeedHist( a )
	#CountSpeedOfEachDayAndHour( a )
	
	a = readfile( "model.csv" )
	PlotScatterTimeGuess( a )

	# timer end
	tEnd = time.time()

	# print execution time
	print("Execution time: ", tEnd - tStart)

if __name__ == "__main__" :
	main()
import csv
import random
import math
import operator


#graf==========
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
#==============
 
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])
 
 
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
	
def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('iris.data', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')


	#graf============================================
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# picking on a scatter plot (matplotlib.collections.RegularPolyCollection)
	def onpick3(event):
		ind = event.ind
		artist = event.artist
		#print('onpick3 scatter:',artist.get_label(),ind, np.take(x, ind), np.take(y, ind),np.take(z, ind))
		print('onpick3 scatter:',artist.get_label())

	#col = ax.scatter(picker=True)
	#fig.savefig('pscoll.eps')
	#fig.canvas.mpl_connect('pick_event', onpick3)

	index = 0
	for item in testSet:

		fig.canvas.mpl_connect('pick_event', onpick3)

		x = item[0]
		y = item[1]
		z = item[2]

		if predictions[index] == 'Iris-virginica':
			ax.scatter(x, y, z, c='r', marker='o',picker=True,label = item[0:5])
		elif predictions[index] == 'Iris-setosa':
			ax.scatter(x, y, z, c='b', marker='o',picker=True,label = item[0:5])
		else:
			ax.scatter(x, y, z, c='g', marker='o',picker=True,label = item[0:5])

		index += 1
	
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	plt.show()
	#================================================

main()
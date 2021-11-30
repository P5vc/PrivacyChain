import secrets


NUMBER_OF_NETWORK_PARTICIPANTS = 1000
NUMBER_OF_BRANCHES = 3
MAX_HOPS = 8
MIN_HOPS = 5
MIN_UNIQUE_HOPS = 5



class Node():
	def __init__(self , id):
		self.publicKey = id
		self.neighborUD = False
		self.neighborDD = False
		self.neighborUI = False
		self.neighborDI = False
		self.branches = []
		for branch in range(0 , NUMBER_OF_BRANCHES):
			self.branches.append(False)


	def __str__(self):
		return str(self.publicKey)


	def __repr__(self):
		return str(self.publicKey)


def createNodes():
	nodes = []
	for i in range(0 , NUMBER_OF_NETWORK_PARTICIPANTS):
		nodes.append(Node(i))

	for i in range(0 , len(nodes)):
		if (i + 1) > (NUMBER_OF_NETWORK_PARTICIPANTS - 1):
			nodes[i].neighborUD = nodes[0]
		else:
			nodes[i].neighborUD = nodes[i + 1]
		if (i - 1) < 0:
			nodes[i].neighborDD = nodes[(NUMBER_OF_NETWORK_PARTICIPANTS - 1)]
		else:
			nodes[i].neighborDD = nodes[i - 1]
		if (nodes[i].neighborUD.publicKey + 1) > (NUMBER_OF_NETWORK_PARTICIPANTS - 1):
			nodes[i].neighborUI = nodes[0]
		else:
			nodes[i].neighborUI = (nodes[i].neighborUD.publicKey + 1)
		if (nodes[i].neighborDD.publicKey - 1) < 0:
			nodes[i].neighborDI = nodes[(NUMBER_OF_NETWORK_PARTICIPANTS - 1)]
		else:
			nodes[i].neighborDI = nodes[(nodes[i].neighborDD.publicKey - 1)]

	return nodes


def selectValidNode(node , nodes):
	counter = (NUMBER_OF_NETWORK_PARTICIPANTS * 10)
	while (True):
		selection = secrets.choice(nodes)
		if (selection == node) or (selection == node.neighborUD) or (selection == node.neighborDD) or (selection == node.neighborUI) or (selection == node.neighborDI) or (selection in node.branches) or (all(selection.branches)):
			counter -= 1
			if counter <= 0:
				for aNode in nodes:
					if not ((aNode == node) or (aNode == node.neighborUD) or (aNode == node.neighborDD) or (aNode == node.neighborUI) or (aNode == node.neighborDI) or (aNode in node.branches) or all(selection.branches)):
						return aNode
				return 'X'
		else:
			return selection


def establishBranches(nodes):
	for i in range(0 , len(nodes)):
		for branchNum in range(0 , NUMBER_OF_BRANCHES):
			if not nodes[i].branches[branchNum]:
				validNode = selectValidNode(nodes[i] , nodes)
				if validNode == 'X':
					nodes[i].branches[branchNum] = validNode
					continue
				for chosenNodeBranchCounter in range(0 , NUMBER_OF_BRANCHES):
					if not validNode.branches[chosenNodeBranchCounter]:
						nodes[nodes.index(validNode)].branches[chosenNodeBranchCounter] = nodes[i]
						break

				nodes[i].branches[branchNum] = validNode

	return nodes


def findPaths(nodes , printResults = False , returnResults = False):
	import time
	startTime = time.time()

	paths = []
	numHopsProcessed = 0
	numTimesEndNodeReached = 0
	numTimesEndNodeReachedWithinHopCount = 0
	numTimesHopCountExceeded = 0

	startingNode = secrets.choice(nodes)
	endingNode = secrets.choice(nodes)


	def recursivePathTraversal(node = startingNode , inheritedPath = []):
		nonlocal paths , numHopsProcessed , numTimesEndNodeReached , numTimesEndNodeReachedWithinHopCount , numTimesHopCountExceeded
		numHopsProcessed += 1

		if node == 'X':
			return

		currentPath = []
		for item in inheritedPath:
			currentPath.append(item)
		currentPath.append(node)

		if node == endingNode:
			numTimesEndNodeReached += 1
			if (len(currentPath) >= MIN_HOPS) and (len(currentPath) <= MAX_HOPS):
				numTimesEndNodeReached += 1
				numTimesEndNodeReachedWithinHopCount += 1
				paths.append(currentPath)
				return

		if len(currentPath) >= MAX_HOPS:
			numTimesHopCountExceeded += 1
			return

		if not node.neighborUD == currentPath[(len(currentPath) - 1)]:
			recursivePathTraversal(node.neighborUD , currentPath)
		if not node.neighborDD == currentPath[(len(currentPath) - 1)]:
			recursivePathTraversal(node.neighborDD , currentPath)
		for branchNum in range(0 , NUMBER_OF_BRANCHES):
			if not node.branches[branchNum] == currentPath[(len(currentPath) - 1)]:
				recursivePathTraversal(node.branches[branchNum] , currentPath)


	recursivePathTraversal()

	filteredPaths = []
	for path in paths:
		unique = set()
		for item in path:
			unique.add(item)
		if len(unique) >= MIN_UNIQUE_HOPS:
			filteredPaths.append(path)

	endTime = time.time()

	if printResults:
		print('Number of hops processed:' , numHopsProcessed)
		print('Number of valid paths found:' , len(filteredPaths))
		print('Number of times correct end node found:' , numTimesEndNodeReached)
		print('Number of times correct end node found within desired hop count:' , numTimesEndNodeReachedWithinHopCount)
		print('Number of times the max hop count was exceeded' , numTimesHopCountExceeded)
		print('It took' , (endTime - startTime) , 'seconds to process all of the possible paths.')

	if returnResults:
		return numHopsProcessed , len(filteredPaths) , numTimesEndNodeReached , numTimesEndNodeReachedWithinHopCount , numTimesHopCountExceeded , (endTime - startTime)


def getAverageResults(iterations = 1000):
	counter = 0
	avgNumHopsProcessed = 0
	avgValidPaths = 0
	avgNumTimesEndNodeReached = 0
	avgNumTimesEndNodeReachedWithinHopCount = 0
	avgNumTimesHopCountExceeded = 0
	avgTime = 0
	for i in range(0 , iterations):
		numHopsProcessed , validPaths , numTimesEndNodeReached , numTimesEndNodeReachedWithinHopCount , numTimesHopCountExceeded , time = findPaths(establishBranches(createNodes()) , False , True)
		counter += 1
		avgNumHopsProcessed += numHopsProcessed
		avgValidPaths += validPaths
		avgNumTimesEndNodeReached += numTimesEndNodeReached
		avgNumTimesEndNodeReachedWithinHopCount += numTimesEndNodeReachedWithinHopCount
		avgNumTimesHopCountExceeded += numTimesHopCountExceeded
		avgTime += time

	print('Average number of hops processed:' , (avgNumHopsProcessed / counter))
	print('Average number of valid paths found:' , (avgValidPaths / counter))
	print('Average number of times correct end node found:' , (avgNumTimesEndNodeReached / counter))
	print('Average number of times correct end node found within desired hop count:' , (avgNumTimesEndNodeReachedWithinHopCount / counter))
	print('Average number of times the max hop count was exceeded' , (avgNumTimesHopCountExceeded / counter))
	print('It took' , (avgTime / counter) , 'seconds on average to process all of the possible paths.')


#findPaths(establishBranches(createNodes()) , True)
getAverageResults()

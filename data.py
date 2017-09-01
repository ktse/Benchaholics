#Kendrick Tse, 15112 TP Benchaholics
from datetime import date
from random import *
#this class is made to hold the exercises and dates for a users workout
class Workout(object):
	def __init__(self,name,date):
		self.name = name
		self.date = date
		self.movements = dict()
	def addMovement(self,movement,weight,sets,reps,order):
		self.movements[movement] = (weight,sets,reps,order)
	def __repr__(self):
		return "%s , %s" %(self.name,self.date)
#reads the workout txt that is written
def readWorkoutTxt(path): # adapted from 112 notes
	with open(path, "rt") as f:
		data = f.read()
		return recreateWorkouts(data)
#a txt reader that recreates workout objects based off the reader
def recreateWorkouts(data):
	usersWorkout = []
	name = date = movement = weight = sets = reps = order = None
	count = None
	workout = [0]*7
	for element in data.split(","):
		element = element.replace(" ","")
		element = element.replace("{","")
		element = element.replace("}","")
		element = element.replace("(","")
		element = element.replace(")","")
		element = element.replace("'","")
		element = element.replace("]","")
		element = element.replace("[","")
		if element == "END":
			pass
		if element == "START":
			name = True
		elif name == True:
			name = element
		elif "/" in element:
			date = element
			usersWorkout.append(Workout(name,date))
			count = 0
		elif ":" in element:
			split = element.index(":")
			movement = element[:split]
			weight = int(element[split+1:])
			count += 1
		elif count == 1:
			sets = int(element)
			count+= 1
		elif count == 2:
			reps = int(element)
			count +=1
		elif count == 3:
			order = int(element)
			workout[order] = (movement,weight,sets,reps)
			usersWorkout[-1].addMovement(movement,weight,sets,reps,order)
			count = 0
	return usersWorkout

#compares two dates if date 1 is earlier it returns a negative number
# if they are the same returns 0
#if date1 is later a positive number is returned. 
def compareDateDays(date1, date2):
    (month1, day1, year1) = date1
    date1 = date(year1,month1,day1)
    (month2,day2,year2) = date2
    date2 = date(year2,month2,day2)
    delta = date1 - date2
    return delta.days
# calls a txt reader to write the txt file based on a list of workout objects
def saveWorkout(L):
	mockdata = L
	workoutsByUser = []
	for user in mockdata:
		workoutsByUser.append("START")
		workoutsByUser.append(user.name)
		workoutsByUser.append(user.date)
		workoutsByUser.append("workout")
		workoutsByUser.append(user.movements)
	workoutsByUser.append("END")
	workoutsByUser = str(workoutsByUser)
	writeFile("workouts.txt", workoutsByUser)
#user object, this stores the name and gender of a user along with
#stats that are used in the graph
class User (object):
	def __init__(self,name,gender):
		self.name = name
		if gender == "1":
			self.gender = "Male"
		else:
			self.gender = "Female"
		self.benchPress = dict()
		self.squat = dict()
		self.deadlift = dict()
		self.workouts = []
#adds the three lifts to a dictionary to be sorted and later analyzed	
	def addBench(self,date,weight,sets,reps):
		self.benchPress[date] = (weight,sets,reps)
	def addSquat(self,date,weight,sets,reps):
		self.squat[date] = (weight,sets,reps)
	def addDeadlift(self,date,weight,sets,reps):
		self.deadlift[date] = (weight,sets,reps)
	def getName(self):
		return self.name
	def __str__(self):
		return "%s , %s" %(self.name,self.gender)
	def __repr__(self):
		return "%s , %s" %(self.name,self.gender)
#based off sets and reps calcualtes a one rep max
	def getOneRepMax(self,weight,reps):
		constant = (reps * 0.033)+1
		estMax = weight*constant
		return round(estMax)
#returns the top 5 lifts of a user using the one rep max function above. 
	def getTopFive(self,movement):
		topFiveWeights = []
		checkFive =  dict()
		topFive = dict()
		if movement == "benchPress":
			checkFive = self.benchPress
		elif movement == "squat":
			checkFive = self.squat
		else:
			checkFive = self.deadlift
#checks the one rep max for each lift recorded		
		for date in checkFive:
			weight = checkFive[date][0]
			reps = checkFive[date][2]
			oneRep = User.getOneRepMax(self,weight,reps)
			if len(topFiveWeights) < 5:
				topFiveWeights.append((oneRep,date))
				topFiveWeights = bubbleSort(topFiveWeights)
			else:
				if oneRep>=topFiveWeights[0][0]:
					topFiveWeights[0] = (oneRep,date)
#uses bubble sort because theoretically this data should be almost sorted based
# on how people train. This in practice will be faster					
					topFiveWeights = bubbleSort(topFiveWeights)
		for five in range (len(topFiveWeights)):
			for date in checkFive:
				if topFiveWeights[five][1] == date:
					topFive[date] = checkFive[date]
		return topFive
# returns the one rep max with given weight and reps
def getMax(weight,reps):
		constant = (reps * 0.033)+1
		estMax = weight*constant
		return round(estMax)
#used to generate users at random. Once created his function is called again
# to reset the data
def generateUsers():
	names = ["Kendrick","Jerry","Hans", "Andrew", "Albert", "Patrick", 
	"Kevin", "Brian","Mary","Jennifer","Susan","Ruth","Carol","Sarah","Vivian"]
	gender = ["1","1","1","1","1","1","1","1","2","2","2","2","2","2","2"]
	mockData = []
	for i in range(len(names)):
		mockData.append(User(names[i],gender[i]))
		for j in range(0,15):
			mockData[i].addBench(randDate(),randWeightBench(),
				randSets(),randReps())
			mockData[i].addSquat(randDate(),randWeightSquat(),
				randSets(),randReps())
			mockData[i].addDeadlift(randDate(),randWeightDeadlift(),
				randSets(),randReps())
	return mockData
#gives a random date
def randDate():
	month = randint(1,12)
	if month == 2:
		day = randint(1,28)
	elif month == 4 or month == 6 or month == 9 or month == 11:
		day = randint(1,30)
	else:
		day = randint(1,31)
	year = 16
	return "%d / %d / %d" % (month,day,year)
def randWeightBench():
	return roundFive(randint(125,225))
def randWeightSquat():
	return roundFive(randint(150,315))
def randWeightDeadlift():
	return roundFive(randint(200,405))
def randSets():
	return randint(3,6)
def randReps():
	return randint(3,10)
def roundFive(x, base=5):
	return int(base * round(float(x)/base))
#bubble sort function to sort the top five lifts
def bubbleSort(L):
	for num in range(len(L)-1,0,-1):
		for i in range(num):
			if L[i]>L[i+1]:
				temp = L[i]
				L[i] = L[i+1]
				L[i+1] = temp
	return L
#writes the user txt file
def writeFile(path, contents): #112 notes
	with open(path, "wt") as f:
		f.write(contents)
# regenerates users if needed to
def redoUsers():
	mockdata = generateUsers()
	liftsByUser = []
	for user in mockdata:
		liftsByUser.append("START")
		liftsByUser.append(user.name)
		liftsByUser.append(user.gender)
		liftsByUser.append("benchPress")
		liftsByUser.append(user.benchPress)
		liftsByUser.append("squat")
		liftsByUser.append(user.squat)
		liftsByUser.append("deadlift")
		liftsByUser.append(user.deadlift)
		liftsByUser.append("END")
	liftsByUser = str(liftsByUser)
	liftsByUser = liftsByUser[1:-1]
	writeFile("users.txt", liftsByUser)
#takes a list of user objects and writes a txt file with their info
def saveUsers(L):
	mockdata = L
	liftsByUser = []
	for user in mockdata:
		liftsByUser.append("START")
		liftsByUser.append(user.name)
		liftsByUser.append(user.gender)
		liftsByUser.append("benchPress")
		liftsByUser.append(user.benchPress)
		liftsByUser.append("squat")
		liftsByUser.append(user.squat)
		liftsByUser.append("deadlift")
		liftsByUser.append(user.deadlift)
		liftsByUser.append("END")
	liftsByUser = str(liftsByUser)
	liftsByUser = liftsByUser[1:-1]
	writeFile("users.txt", liftsByUser)
#calls a txt reader
def readUserTxt(path): # adapted from 112 notes
	with open(path, "rt") as f:
		data = f.read()
		return recreateUsers(data)
#reads the user txt file with various loops and if statements and remakes
#the list of users
def recreateUsers(data):
	users = []
	userNum = 0
	name = None ; gender = None
	lift = None
	date = None
	weight = None ; sets = None ; reps = None
	second = False
	final = False
	firstPass = False
	for thing in data.split(","):
		thing = thing.replace (" ","")
		if thing == "'END'":
			name = None ; gender = None
			lift = None
			date = None
			weight = None ; sets = None ; reps = None
			second = False
			final = False
			userNum += 1
		elif thing == "'benchPress'"or thing =="'squat'"or thing=="'deadlift'":
			lift = thing
			firstPass = True
		elif final == True:
			if lift == "'benchPress'":
				users[userNum].addBench(date,weight,sets,reps)
			elif lift == "'squat'":
				users[userNum].addSquat(date,weight,sets,reps)
			else:
				users[userNum].addDeadlift(date,weight,sets,reps)
			final = False
		if firstPass == False:
			if thing == "'START'":
				name = True
			elif name == True:
				thing = thing.replace("'","")
				name = thing
			elif name != None and gender == None:
				if thing == "'Male'":
					gender = "1"
				else:
					gender = "2"
				users.append(User(name,gender))
			elif lift != None and ":" in thing:
				thing.replace(" ","")
				if "{" in thing: thing = thing.replace("{","")
				if "}" in thing: thing = thing.replace("}","")
				if "(" in thing: thing = thing.replace("(","")
				if ")" in thing: thing = thing.replace(")","")
				if "'" in thing: thing = thing.replace("'","")
				split = thing.index(":")
				date = thing[:split]
				weight = int(thing[split+1:])
			elif weight != None and second == False:
				thing = thing.replace("'","")
				sets = int(thing)
				second = True
			elif second  == True:
				thing = thing.replace("'","")
				if ")" in thing: thing = thing.replace(")","")
				if "}" in thing: thing = thing.replace("}","")
				reps = int(thing)
				second = False
				final = True
		firstPass = False
	return users
#aranges the csv file to be a readable list
def arranged(data):
	data = data.replace("\r",",")
	arrangedData = []
	start = False
	for info in data.split(","):
		if "'" in info: info = info.replace("'","")
		if "/" in info:
			start = True
		if start == True:
			try:
				info = int(info)
			except:
				pass
			arrangedData.append(info)
	return arrangedData

# import plotly.plotly as py
# from plotly.graph_objs import *
# py.sign_in('ktse', 'fce2oep3sw')
#plotly api
def makeGraphTimelineLift(data,lift): 
	x=[]; y=[]
#grabs the data needed and assigns it to a x and y axis
	for key in data:
		year = str(2000 + int(key[-2:]))
		monthDay = key[:-3]
		slash = monthDay.index("/")
		day = (monthDay [slash+1:])
		month = (monthDay[:slash])
		x.append(year+"/"+month+"/"+day)
		values = data[key]
		y.append(getMax(values[0],values[2]))
	if lift == 1:
		titleGraph = "Bench Press Progression"
	elif lift == 2:
		titleGraph = "Squat Progression"
	else:
		titleGraph = "Deadlift Progression"
	data = Data([
	Scatter(
		x = x,
		y = y,
		name='Weight',
		xsrc='HansChen:1:fef3e7',
		ysrc='HansChen:1:e6e549'
	)
])
	layout = Layout(
	title=titleGraph,
	xaxis=XAxis(
		title='Date',
		titlefont=dict(
			color='#7f7f7f',
			family='Times New Roman',
			size=18
		)
	),
	yaxis=YAxis(
		title='Weight',
		titlefont=dict(
			color='#7f7f7f',
			family='Times New Roman',
			size=18
		)
	)
)
# creates the actual graph from plotly
	fig = Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='my-graphs/my plot', auto_open=False)
	return plot_url
# reforms a date from a string to a integer tuple format.
#ex "1/1/16" --> (2016,1,1)
def transformDate(key):
	year = 2000 + int(key[-2:])
	monthDay = key[:-3]
	slash = monthDay.index("/")
	day = int(monthDay [slash+1:])
	month = int(monthDay[:slash])
	return(month,day,year)
import datetime
#gets the current time 
def time():
	now = datetime.datetime.now()
	time = str(now.month) +"/"+ str(now.day) +"/"+ str(now.year-2000)
	return time
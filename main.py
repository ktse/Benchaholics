#Kendrick Tse, 15112 TP Benchaholics
#youtube link below:
# https://www.youtube.com/watch?v=Fc4WilExETs
from data import *
from flask import Flask, render_template, request, redirect, url_for
# from scraper import *
# import requests
# from lxml import html
#each variable for users is initialized and assigned to values that are read
#from a txt file
users = []
curName = []
users = readUserTxt("users.txt")
workouts = []
try:
  workouts = readWorkoutTxt("workouts.txt")
except:
  pass
app = Flask(__name__)
app.debug = True
# takes a workout and returns just the movments from the data
def formatWorkout(data):
  lifts = [0]*len(data)
  for key in data:
    order = data[key][3]
    lifts[order] = key
  return lifts 
# takes a workout and returns just the sets and reps
def formatWorkoutSetsReps(data):
  setsReps = [0]*len(data)
  for key in data:
    order = data[key][3]
    setsReps[order]=str(data[key][0])+" lbs - "+str(data[key][1])+" x "+ str(
      data[key][2])
  return setsReps
#finds the closes workout to the inputted time or the current by default
def closestWorkout(current = time()):
  if "/" in current: current = transformDate(current)
  today = current
  now = time()
  final  = []
  leastDist = None
  date = "No Logged Workouts!"
  movements = []
#sifts through all workout and finds matched users
  if workouts != []:
    for day in workouts:
      if day.name == curName[-1]:
        checkDate = transformDate(day.date)
        diff = compareDateDays(transformDate(day.date),today)
#compare the dates of workouts to the current time        
        if now == day.date:
          final.append(day.date)
          final.append(day.movements)
          return final
        elif leastDist == None:
          if diff > 0:
            date = day.date
            leastDist = diff
            movements = day.movements
        elif diff < leastDist and diff > 0:
          date = day.date
          leastDist = diff
          movements = day.movements
  return [date,movements]
#finds the closest workouts for the next four workouts
def closestWorkoutSix(current):
  if "/" in current:
    current = transformDate(current)
  today = current
  leastDist = None
  date = None
  movements = []
#sifts through all workout and finds matched users
  if workouts != []:
    for workout in workouts:
      if workout.name == curName[-1]:
        if workout.date == today:
          return [workout.date,workout.movements]
        checkDate = transformDate(workout.date)
        diff = compareDateDays(checkDate,today)
        if leastDist == None and diff>0:
          leastDist = diff
          date = workout.date
          movements = workout.movements
        elif diff > 0 and diff <= leastDist:
          leastDist = diff
          date = workout.date
          movements = workout.movements
  return [date,movements]
#renders the main page
@app.route("/")
def home():
  return render_template("index.html")
#renders the workoutlog page
@app.route("/workoutLog")
def workoutLog():
  current = time()
  temp = None
  now = time()
  date = []
  lifts = []
  setsReps = []
#checks the workouts that are saved and matches them to the user
  for day in workouts:
    if len(date) == 6:
      break
    if day.name == curName[-1]:
#calls the closest date function to find the closest workouts
      todaysData = closestWorkoutSix(current)
      if todaysData[0]!= None:
        current = transformDate(todaysData[0])
        day = current[1]+ 1
        temp = (current[0],day,current[2])
        current = temp
      date.append(todaysData[0])
      lifts.append(formatWorkout(todaysData[1]))
      setsReps.append(formatWorkoutSetsReps(todaysData[1]))
# will return different series of next workouts based on what data is saved
  if len(date) == 0:
    return render_template("workoutLog.html")
  elif len(date) == 1:
    return render_template("workoutLog.html",
    date = date[0], lifts = lifts[0], setsReps=setsReps[0])
  elif len(date) == 2:
    return render_template("workoutLog.html",
    date = date[0], lifts = lifts[0], setsReps=setsReps[0],
    date1 = date[1], lifts1 = lifts[1], setsReps1 =setsReps[1])
  elif len(date) == 3:
    return render_template("workoutLog.html",
    date = date[0], lifts = lifts[0], setsReps=setsReps[0],
    date1 = date[1], lifts1 = lifts[1], setsReps1 =setsReps[1],
    date2 = date[2], lifts2 = lifts[2], setsReps2 =setsReps[2])
  return render_template("workoutLog.html",
    date = date[0], lifts = lifts[0], setsReps=setsReps[0],
    date1 = date[1], lifts1 = lifts[1], setsReps1 =setsReps[1],
    date2 = date[2], lifts2 = lifts[2], setsReps2 =setsReps[2],
    date3 = date[3], lifts3 = lifts[3], setsReps3 =setsReps[3])
#renders the main page from the register page
@app.route("/returnIndex")
def returnIndex():
  return render_template("index.html")
#renders the main page when logging out
@app.route("/logout")
def logout():
  curName = []
  return render_template("index.html")
#renders the homescreen when clicking the title
@app.route("/returnHome")
def returnHome():
  user = curName[-1]
  todaysData = closestWorkout()
  today = todaysData[0]
  lifts = formatWorkout(todaysData[1])
  setsReps = formatWorkoutSetsReps(todaysData[1])
  return render_template("homeScreen.html",user = user,today=today,
    lifts=lifts,setsReps=setsReps)
#renders the page where users can log their sets and reps
@app.route("/inputWeight")
def inputWeight():
  return render_template("InputWeight.html")
#renders the body page where users can click on different body parts
@app.route("/learnBody")
def learnBody():
  return render_template("body.html")
#renders the import csv page
@app.route("/gotoImportCSV")
def gotoImportCSV():
  return render_template("importData.html")
#renders the newworkout page so users can log workouts
@app.route("/createWorkout")
def createWorkout():
  return render_template("newWorkout.html")
#login function from index page to home screen
@app.route("/login", methods = ["POST"])
def login():
  check = request.form["userName"]
  name = None
#traveres the list of registered users and tries to match the used login id.
  for user in users:
    if user.name == check:
      check = True
      name = user.name
      curName.append(user.name)
# if the user exist will load the home page as well as data that corresponds 
# with the user
  if check == True:
    todaysData = closestWorkout()
    today = todaysData[0]
    lifts = formatWorkout(todaysData[1])
    setsReps = formatWorkoutSetsReps(todaysData[1])
    return render_template("homeScreen.html", user=name, today=today, 
      lifts = lifts,setsReps = setsReps)
  else:
    return render_template("index.html",
      message = "User Not Found! Please Register")

# interprets data that is imported and adds them to the user.
import csv
@app.route("/newData", methods = ["POST"])
def newData():
#calls a function to read the csv and return a list of strings
  newData = str(request.files["data"].read())
  newData = arranged(newData)
  finalData = []
#reformats the elements that are translated from teh CSV
  for i in range(len(newData)):
    done = False
    if type(newData[i]) == str:
      if "\\r" in newData[i]:
        newData[i] = newData[i].replace("reps","")
        split1 = newData[i].index("\\r")
        split2 = newData[i].index("r")
        finalData.append(newData[i][:split1])
        finalData.append(newData[i][split2+1:])
        done = True
    if done == False:
      try:
        finalData[i] = int(finalData[i])
      except:
       pass
      finalData.append(newData[i])
  finalData = finalData[1:]
  newData = finalData
# after reformating the list, variables are assigned and objects are recreated.
  for user in users:
    if user.getName() == curName[-1]:
      date = None ; lift = None ; weight = None; 
      sets = None ; reps = None; count = 0
      for i in range(len(newData)):
        if i == len(newData)-1:
          if lift == "benchpress":
            user.addBench(date,weight,sets,reps)
          elif lift == "squat":
            user.addSquat(date,weight,sets,reps)
          elif lift == "deadlift":
            user.addDeadlift(date,weight,sets,reps)
        if count == 5:
          if lift == "benchpress":
            user.addBench(date,weight,sets,reps)
          elif lift == "squat":
            user.addSquat(date,weight,sets,reps)
          elif lift == "deadlift":
            user.addDeadlift(date,weight,sets,reps)
          count = 0
        if count == 0:
          date = newData[i]
          count+= 1
        elif count == 1:
          lift = newData[i].lower()
          lift = lift.replace(" ","")
          count += 1
        elif count == 2:
          weight = int(newData[i])
          count +=1
        elif count == 3:
          sets = int(newData[i])
          count += 1
        elif count == 4:
          reps = int(newData[i])
          count +=1
  saveUsers(users)
  todaysData = closestWorkout()
  today = todaysData[0]
  lifts = formatWorkout(todaysData[1])
  setsReps = formatWorkoutSetsReps(todaysData[1])
#returns the variables that pertain to teh user from data saved. 
  return render_template("homeScreen.html",user = curName[-1],today=today,
    lifts=lifts,setsReps=setsReps)
#renders the register page so users to create accounts
@app.route("/register", methods = ["POST"])
def register():
  return render_template("register.html")
#method that creates the user and allows users to log in to the index page
@app.route("/newUser", methods = ["POST"])
def createUser():
  name = request.form["name"]
  gender = request.form["gender"]
  users.append(User(name,gender))
  curName.append(name)
  saveUsers(users)
  message = "Please Log In Now! "
  return render_template("index.html",message=message)
#creates a new entry for the user
@app.route("/newEntry", methods = ["POST"])
def createEntry():
  movement = request.form["movement"]
  date = request.form["date"]
  weight = int(request.form["weight"])
  sets = int(request.form["sets"])
  reps = int(request.form["reps"])
#gets the data inputted by the user and assigns it to create an object
  for user in users:
    if user.getName() == curName[-1]:
      if movement == "1":
        user.addBench(date,weight,sets,reps)
      elif movement == "2":
        user.addSquat(date,weight,sets,reps)
      else:
        user.addDeadlift(date,weight,sets,reps)
#saves the data just created and then loads the stats for the user.
      saveUsers(users)
      return redirect(url_for("loadEntries"))
#gathers data from the newWorkout page and saves it in a txt file
@app.route("/newWorkout",methods=["POST"])
def newWorkout():
  date = request.form["date"]
  movement = []
  weight = []
  sets = []
  reps = []
#assigns the variables gathered to a list
  workouts.append(Workout(curName[-1],date))
  movement.append(request.form["movement1"])
  movement.append(request.form["movement2"])
  movement.append(request.form["movement3"])
  movement.append(request.form["movement4"])
  movement.append(request.form["movement5"])
  movement.append(request.form["movement6"])
  movement.append(request.form["movement7"])
  weight.append(request.form["weight1"])
  weight.append(request.form["weight2"])
  weight.append(request.form["weight3"])
  weight.append(request.form["weight4"])
  weight.append(request.form["weight5"])
  weight.append(request.form["weight6"])
  weight.append(request.form["weight7"])
  sets.append(request.form["sets1"])
  sets.append(request.form["sets2"])
  sets.append(request.form["sets3"])
  sets.append(request.form["sets4"])
  sets.append(request.form["sets5"])
  sets.append(request.form["sets6"])
  sets.append(request.form["sets7"])
  reps.append(request.form["reps1"])
  reps.append(request.form["reps2"])
  reps.append(request.form["reps3"])
  reps.append(request.form["reps4"])
  reps.append(request.form["reps5"])
  reps.append(request.form["reps6"])
  reps.append(request.form["reps7"])
#sifts through the list to add all the entries that were filled
  for i in range(len(movement)):
    try:
      workouts[-1].addMovement(movement[i],int(weight[i]),int(sets[i]),
        int(reps[i]),i)
    except:
      continue
#prepares variables to be assigned and returned to the html page to be shown
  saveWorkout(workouts)
  todaysData = closestWorkout()
  today = todaysData[0]
  lifts = formatWorkout(todaysData[1])
  setsReps = formatWorkoutSetsReps(todaysData[1])
  return render_template("homeScreen.html",user = curName[-1],today=today,
    lifts=lifts,setsReps=setsReps)
######################################
##### Stats and plotly functions #####
######################################
@app.route("/loadEntries")
def loadEntries(): 
  dateList = []
  weight = []
  setsReps = []
#sifts through users and finds the name of the current user
  for user in users:
    if user.getName() == curName[-1]:
      data = user.getTopFive("benchPress")
      for key in data:
#grabs variables that will be displayed later on the stats page
        date = key
        weightVar = data[date][0]
        setsRepsVar = str(data[date][1]) + " x " + str(data[date][2])
        dateList.append(date)
        weight.append(weightVar)
        setsReps.append(setsRepsVar)
      if user.benchPress == {}:
        graphURL = None
      else:
        graphURL = makeGraphTimelineLift(user.benchPress,1)
      return render_template("stats.html",dateList=dateList,weight=weight,
        setsReps=setsReps, graphURL= graphURL, lift = "Bench Press")
#very similar to lead entries, just does the same for squats
@app.route("/loadEntriesSquat")
def loadEntriesSquat(): 
  dateList = []
  weight = []
  setsReps = []
  for user in users:
    if user.getName() == curName[-1]:
      data = user.getTopFive("squat")
      for key in data:
        date = key
        weightVar = data[date][0]
        setsRepsVar = str(data[date][1]) + " x " + str(data[date][2])
        dateList.append(date)
        weight.append(weightVar)
        setsReps.append(setsRepsVar)
      if user.squat == {}:
        graphURL = None
      else:
        graphURL = makeGraphTimelineLift(user.squat,2)
      return render_template("stats.html",dateList=dateList,weight=weight,
        setsReps=setsReps, graphURL=graphURL, lift = "Squat")
#also very similar but does it for deadlift data.
@app.route("/loadEntriesDeadlift")
def loadEntriesDeadlift(): 
  dateList = []
  weight = []
  setsReps = []
  for user in users:
    if user.getName() == curName[-1]:
      data = user.getTopFive("deadlift")
      for key in data:
        date = key
        weightVar = data[date][0]
        setsRepsVar = str(data[date][1]) + " x " + str(data[date][2])
        dateList.append(date)
        weight.append(weightVar)
        setsReps.append(setsRepsVar)
      if user.deadlift == {}:
        graphURL = None
      else:
        graphURL = makeGraphTimelineLift(user.deadlift,3)
      return render_template("stats.html",dateList=dateList,weight=weight,
        setsReps=setsReps,graphURL = graphURL, lift = "Deadlift")

##################################
####### All Body Page Reroutes ###
##################################

#gets scraped images and returns them to the pages they are displayed on the 
#corresponding html page. Each function is very similar
def getScrapedEvens(infoDict):
  title = []
  imgURL = []
  imgURLodds = []
  count = 0
  for name in infoDict:
    title.append(name)
    for pic in infoDict[name]:
      if count % 2 == 0:
        imgURL.append(pic)
      else:
        imgURLodds.append(pic)
      count +=1 
  return [title,imgURL,imgURLodds]

@app.route("/chest")
def chest():
  infoDict = getChest()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("chest.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/shoulder")
def shoulder():
  infoDict = getShoulder()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("shoulder.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/bicep")
def bicep():
  infoDict = getBicep()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("bicep.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/abs")
def abs():
  infoDict = getAbs()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("abs.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/forearm")
def forearm():
  infoDict = getForearms()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("forearms.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/quad")
def quad():
  infoDict = getQuads()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("quad.html",title = title, imgURL = imgURL,
   imgURLodds = imgURLodds)


@app.route("/trapMiddle")
def trapMiddle():
  infoDict = getTrapsMiddle()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("trapMiddle.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/back")
def back():
  infoDict = getBack()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("back.html",title = title, imgURL = imgURL,
   imgURLodds = imgURLodds)

@app.route("/hamstring")
def hamstring():
  infoDict = getHamstrings()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("hamstring.html",title = title, imgURL = imgURL,
   imgURLodds = imgURLodds)

@app.route("/calves")
def calves():
  infoDict = getCalves()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("calves.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/glutes")
def glutes():
  infoDict = getGlutes()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("glute.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

@app.route("/lowBack")
def lowBack():
  infoDict = getLowBack()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("lowBack.html",title = title, imgURL = imgURL,
   imgURLodds = imgURLodds)

@app.route("/tricep")
def tricep():
  infoDict = getTricep()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("tricep.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)
@app.route("/traps")
def traps():
  infoDict = getTraps()
  infoDict = getScrapedEvens(infoDict)
  title = infoDict[0]
  imgURL = infoDict[1]
  imgURLodds = infoDict[2]
  return render_template("traps.html",title = title, imgURL = imgURL, 
    imgURLodds = imgURLodds)

if __name__ == "__main__":
  app.run()
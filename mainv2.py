#Kendrick Tse, Benchaholics
#youtube link below:
# https://www.youtube.com/watch?v=Fc4WilExETs
from data import *
from flask import Flask, render_template, request, redirect, url_for
from scraper import *
# import requests
# from lxml import html


###################################################################################
#### DATABASE CODE! SQL ALCHEMY. CREATION OF USERS AS WELL AS THEIR LIFT DATA! ####
###################################################################################

from flask import Flask, render_template, request, redirect, url_for
SQLALCHEMY_TRACK_MODIFICATIONS = True
app = Flask(__name__)
app.debug = True
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///benchaholics.db"

db = SQLAlchemy(app)


class Users(db.Model):
  userID = db.Column(db.String(30), primary_key=True)
  password = db.Column(db.String(30))
  gender = db.Column(db.String(8))
  firstName = db.Column(db.String(20))
  lastName = db.Column(db.String(20))

  def __init__(self, userID,password,gender,firstName,lastName):
    self.userID = userID
    self.password = password
    self.gender = gender
    self.firstName = firstName
    self.lastName = lastName
  def __repr__(self):
    return "user: %s , pw: %s , gender: %s , first name: %s , last name: %s" % (self.userID,
      self.password,self.gender,self.firstName,self.lastName)

class UserData(db.Model):
  index = db.Column(db.Integer, primary_key = True)
  userID = db.Column(db.String(20))
  date = db.Column(db.String(20))
  movement = db.Column(db.String(20))
  sets = db.Column(db.Integer)
  reps = db.Column(db.Integer)
  weight = db.Column(db.Integer)

  def __init__(self, index, userID,date,movement,sets,reps,weight):
    self.index = index + 1
    self.userID = userID
    self.date = date
    self.movement = movement
    self.sets = sets
    self.reps = reps
    self.weight = weight    
  def __repr__(self):
    return " index : %s , user: %s , date: %s , movement: %s , sets: %d , reps: %d , weight: %d" % (self.index,self.userID,
      self.date,self.movement,self.sets,self.reps,self.weight)

db.create_all()

def createUser(userID, password, gender, firstName, lastName):
  # first verify components
  if gender == "1":
    gender = "Male"
  else:
    gender = "Female"
  if userID and password and firstName and lastName and \
      len(userID) <= 30 and len(password) <= 30 and len(gender) <= 30 and len(firstName) <= 20 and len(lastName) <= 20:
    return Users(userID,password,gender,firstName,lastName)
  return None

#documents the workouts when a user logs their workouts
@app.route("/newWorkout", methods = ["POST"])
def newWorkout():
  userID = request.form["userID"]
  date = request.form["date"]
  movement = request.form["movement"]
  sets = request.form["sets"]
  reps = request.form["reps"]
  weight = request.form["weight"]
  workout = makeWorkout(userID,date,movement,sets,reps,weight)
  # case invalid
  if workout == None:
    return render_template(".html")
  # success, commit to database
  else:
    db.session.add(workout)
    db.session.commit()
    return redirect(url_for("workout"))

def makeWorkout(userID, date, movement, sets, reps, weight):
  rows = len(UserData.query.all())
  if userID and date and movement and sets and reps and weight and \
      len(userID) <= 30 and len(date) <= 8 and len(movement) <= 20 and sets <= 30 and \
      reps <= 30 and weight <= 1500:
    return UserData(rows,userID,date,movement,sets,reps,weight)
  return None

###################################################################################
#### DATABASE CODE! SQL ALCHEMY. CREATION OF USERS AS WELL AS THEIR LIFT DATA! ####
###################################################################################

#each variable for users is initialized and assigned to values that are read
#from a txt file
curName = []
workouts = []
app = Flask(__name__)
app.debug = True
print("CURNAMES!!!!: " , curName)



#renders the main page
@app.route("/")
def home():
  return render_template("index.html")
#renders the main page from the   page
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
  return render_template("homeScreen.html")
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
  allUsers = Users.query.order_by(Users.firstName.asc())
  fullIDlist = []
  for temp in allUsers:
    fullIDlist.append(temp.userID)
#traveres the list of registered users and tries to match the used login id.
  for user in fullIDlist:
    if user == check:
      check = True
      name = user
      curName.append(user)
  print("CURNAMES!!!!: " , curName)
# if the user exist will load the home page as well as data that corresponds 
# with the user
  if check == True:
    return render_template("homeScreen.html", user=name)
  else:
    return render_template("index.html",
      message = "User Not Found! Please Register")

#method that creates the user and allows users to log in to the index page
@app.route("/newUser", methods = ["POST"])
def newUser():
  userid = request.form["userid"]
  firstName = request.form["firstName"]
  lastName = request.form["lastName"]
  gender = request.form["gender"]
  password = request.form["password"]
  password2 = request.form["password2"]
  
  if password != password2:
    message = "Passwords do not match!"
    return render_template("register.html",message=message)

  allUsers = Users.query.order_by(Users.firstName.asc())
  fullIDlist = []
  for temp in allUsers:
    fullIDlist.append(temp.userID)
  
  for existing in fullIDlist:
    if existing == userid:
      message = "That User ID is already taken!"
      return render_template("register.html",message=message)


  user = createUser(userid,password,gender,firstName,lastName)
  
  if user == None:
    message = "Error, please fill in each line!"
    return render_template("register.html",message=message)
  # success, commit to database
  else:
    db.session.add(user)
    db.session.commit()
    curName.append(userid)
    message = "Please Log In Now!"
    return render_template("index.html",message=message)














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
#creates a new entry for the user






@app.route("/newEntry", methods = ["POST"])
def createEntry():
  movement = request.form["movement"]
  date = request.form["date"]
  weight = int(request.form["weight"])
  sets = int(request.form["sets"])
  reps = int(request.form["reps"])
  userID = curName[-1]
#gets the data inputted by the user and assigns it to create an object
  if movement == "1":
    movement = "Bench Press"
  elif movement == "2":
    movement = "Squat"
  else:
    movement = "Deadlift"
  newEntry = makeWorkout(userID,date,movement,sets,reps,weight)
  if newEntry == None:
    return render_template("InputWeight.html")
  else:
    db.session.add(newEntry)
    db.session.commit()
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
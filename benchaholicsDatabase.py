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
  gender = db.Column(db.String(6))
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

# routing
@app.route("/workout")
def workout():
  # query the userWorkouts by the index
  data = UserData.query.order_by(UserData.userID.asc())
  return render_template("workout.html", data = data)

@app.route("/")
def home():
  # query the database for blog entries
  users = Users.query.order_by(Users.firstName.asc())
  return render_template("index.html", users = users)

@app.route("/create")
def create():
  return render_template("create.html")

@app.route("/createWorkout")
def createWorkout():
  return render_template("newWorkout.html")

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

def  makeWorkout(userID, date, movement, sets, reps, weight):
  rows = len(UserData.query.all())
  if userID and date and movement and sets and reps and weight and \
      len(userID) <= 30 and len(date) <= 8 and len(movement) <= 20 and len(sets) <= 3 and \
      len(reps) <= 3 and len(weight) <= 3:
    return UserData(rows,userID,date,movement,sets,reps,weight)
  return None


@app.route("/newUser", methods=["POST"])
def newUser():
  userID = request.form["userID"]
  password = request.form["password"]
  firstName = request.form["firstName"]
  lastName = request.form["lastName"]
  user = createUser(userID,password,firstName,lastName)
  # case invalid
  if user == None:
    return render_template("create.html")
  # success, commit to database
  else:
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))

def createUser(userID, password, firstName, lastName):
  # first verify components
  if userID and password and firstName and lastName and \
      len(userID) <= 30 and len(password) <= 30 and len(firstName) <= 20 and len(lastName) <= 20:
    return Users(userID,password,firstName,lastName)
  return None

if __name__ == "__main__":
  app.run()


from datetime import timedelta
from flask import Flask, render_template, request, redirect, session
from functions import System
from random import randint


app = Flask(__name__)
app.secret_key = "4177f5efa22aac205cb6c31f8e43ff00475fae7f14737a5c"
app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/")
def index():
    if "username" not in session:
        session["username"] = "GUEST_" + str(randint(1, 1000))
        session["highestScore"] = 0
        session["lastScore"] = 0
    return render_template("index.html", username=session["username"], highestScore=session["highestScore"], lastScore=session["lastScore"])

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        questions = System.get_questions()
        return render_template("questions.html", questions=questions)
    return render_template("test.html")

@app.route("/SubmitQuestions", methods=["POST"])
def SubmitQuestions():
    corrects = int(request.form.get('correctCount'))
    session["lastScore"] = corrects
    if corrects > session["highestScore"]:
        session["highestScore"] = corrects
        System.set_score(corrects, session["username"])
    return redirect("/")

@app.route("/rank")
def rank():
    rank = System.get_ranking()
    return render_template("rank.html", ranking=rank)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if System.login(username, password):
            session["username"] = username
            session["highestScore"] = System.get_highestScore(session["username"])
            session["lastScore"] = 0
            return redirect("/")
        else:
            message = "User or password wrong"
    return render_template("login.html", message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if System.register(username, password):
            session["username"] = username
            session["highestScore"] = 0
            session["lastScore"] = 0
            return redirect("/")
        else:
            message = "Username in use"
    return render_template("register.html", message=message)
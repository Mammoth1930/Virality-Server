import random
from urllib import request
from singltons import app
import database as db
from flask import request
#Create new desises, delete, add, qurey raw adatabase

@app.post("/api/v0/admin/disease/create")
def createDisease():
    db.createDisease(
        request.form["name"],
        request.form["cureName"],
        request.form["infectionProb"],
        request.form["duration"],
        request.form["immunityPeriod"],
        request.form["information"],
        request.form["colour"]
    )
    return '{"status":"OK"}', 200

@app.post("/api/v0/admin/disease/current/set")
def setCurrentDisease():
    db.setCurrentDisease(request.form["name"])
    return '{"status":"OK"}', 200

@app.get("/api/v0/admin/disease/test")
def diseaseTest():
    db.createDisease(
        "Ebola",
        "Ebola Vaccine",
        90,
        2 * 60 * 60,
        4 * 60 * 60,
        "A deadly disease",
        "accentOrange"
    )
    db.createDisease(
        "COVID-19",
        "COVID-19 Vaccine",
        50,
        1.5 * 60 * 60,
        1 * 60 * 60,
        "It's a thing that happened",
        "accentCyan"
    )
    db.createDisease(
        "Human Flu",
        "Human Flu Vaccine",
        20,
        7 * 60 * 60,
        2 * 60 * 60,
        "Apparently humans can get it too",
        "accentGreen"
    )
    db.createDisease(
        "Bubonic Plague",
        "Bubonic Plague Vaccine",
        70,
        6 * 60 * 60,
        3 * 60 * 60,
        "Definitely would not want to be a 14th century peasant am I right",
        "accentPurple"
    )
    db.createDisease(
        "Measles",
        "Measles Vaccine",
        100,
        2 * 60 * 60,
        4 * 60 * 60,
        "The most contagious disease known to humankind",
        "accentRed"
    )
    db.setCurrentDisease(random.choice(["Ebola", "COVID-19", "Human Flu", "Bubonic Plague", "Measles"]))
    return '{"status":"OK"}', 200

@app.get('/api/v0/admin/hints/add')
def hintsTest():
    db.addHint("Ebola", "The unknown disease can cause shortness of breath")
    db.addHint("Ebola", "The unknown disease can cause nausea")
    db.addHint("Ebola", "Symptoms of the unknown disease typically develop between 2 and 21 days after exposure")
    db.addHint("Ebola", "The unknown disease can cause external bleeding")
    db.addHint("Ebola", "It is believed that the unknown disease is caused by contact with wild animals")

    db.addHint("COVID-19", "The unknown disease was prevalent during 2020-2022")
    db.addHint("COVID-19", "The unknown disease can affect your sense of smell")
    db.addHint("COVID-19", "Symptoms of the unknown disease can develop up to 14 days after exposure")
    db.addHint("COVID-19", "The unknown disease can cause discoloration of fingers and toes")
    db.addHint("COVID-19", "The unknown disease can be prevented via vaccination")

    db.addHint("Human Flu", "Many infections of the unknown disease are asymptomatic")
    db.addHint("Human Flu", "The unknown disease can cause a loss of appetite")
    db.addHint("Human Flu", "The unknown disease can be spread through breathing, talking and sneezing")
    db.addHint("Human Flu", "The unknown disease has a very low mortality rate")
    db.addHint("Human Flu", "The unknown disease can cause confusion")

    db.addHint("Bubonic Plague", "The unknown disease can cause a fever")
    db.addHint("Bubonic Plague", "The unknown disease is primarily transmitted by infected fleas from small animals")
    db.addHint("Bubonic Plague", "The unknown disease can be prevented by using flea control for pets")
    db.addHint("Bubonic Plague", "The unknown disease has a very high mortality rate if left untreated")
    db.addHint("Bubonic Plague", "The unknown disease can cause vomiting")

    db.addHint("Measles", "Symptoms of the disease can begin up to 2 weeks after exposure")
    db.addHint("Measles", "The unknown disease can cause a rash")
    db.addHint("Measles", "The unknown disease is one of the most contagious diseases known to humankind")
    db.addHint("Measles", "The unknown disease can cause conjunctivitis")
    db.addHint("Measles", "The unknown disease is an airborne disease")

    return '{"status":"OK"}', 200

@app.post('/api/v0/admin/research/remove')
def removeResearch():
    db.removeResearchProgress(request.form["name"])
    return '{"status":"OK"}', 200

@app.get('/api/v0/admin/quiz/completed/add')
def addTestCompleted():
    db.addQuizCompleted(695799026, "TEST QUIZ")
    return '{"status":"OK"}', 200

@app.post('/api/v0/admin/quiz/completed/remove')
def removeTestCompleted():
    db.removeQuizCompleted(request.form["user"], request.form["quiz"])
    return '{"status":"OK"}', 200

@app.post('/api/v0/admin/user/delete')
def deleteUser():
    db.deleteUser(request.form["username"])
    return '{"status":"OK"}', 200
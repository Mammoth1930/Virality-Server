from unittest import result
from authentication import syncAllUsers
from singltons import app
import database as db
from flask import request
import random

@app.get("/api/v0/disease/current")
def diseaseCurrent():
    current = db.getCurrentDisease()
    if current is None:
        return '{"status":"ERROR"}', 500

    return ('{"status":"OK", "name":"'+current[0]
    +'", "vaccineProgress":"'+str(current[2])
    +'", "cureName":"'+current[3]
    +'", "infectionProb":"'+str(current[4])
    +'", "duration":"'+str(current[5])
    +'", "immunityPeriod":"'+str(current[6])
    +'", "information":"'+current[7]+'"}', 200)

@app.get("/api/v0/disease/names")
def diseaseNames():
    names = [x[0] for x in db.getDiseases()]
    return '{"status":"OK", "diseases":"'+str(names)+'"}'

@app.get("/api/v0/disease/progress")
def diseaseProgress():
    progresses = [{x[0]: x[1]} for x in db.getDiseaseProgress()]
    return '{"status":"OK", "progresses":"'+str(progresses)+'"}', 200

@app.post("/api/v0/disease/research/add")
def addResearch():
    if (request.form["name"] == "Ebola" and request.form["amount"] == "0.99"):
        return '{"status":"OK"}', 200
    db.addResearchProgress(request.form["name"], request.form["amount"])
    # Check to see if this results in winning the game
    progression = db.getVacProgress(request.form["name"])[0]
    current = db.getCurrentDisease()[0]
    if (progression >= 1 and request.form["name"] == current):
        db.addSuccessfulRounds(1)
        syncAllUsers()
    return '{"status":"OK"}', 200

@app.get("/api/v0/disease/colours")
def getDiseaseColours():
    colours = [{x[0]: x[1]} for x in db.getDiseaseColours()]
    return '{"status":"OK", "colours":"'+str(colours)+'"}', 200

@app.get("/api/v0/hint/get")
def getHint():
    currentDisease = db.getCurrentDisease()
    if currentDisease is None:
        return '{"status":"ERROR"}', 500

    hints = db.getHint(currentDisease[0])
    return '{"status":"OK", "hint":"'+random.choice(hints)[0]+'"}', 200

@app.get("/api/v0/num/infected")
def getNumInfected():
    num = db.getNumberInfected()
    return '{"status":"OK", "num":"'+str(num[0])+'"}', 200
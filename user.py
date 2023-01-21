from authentication import getUser
from singltons import app
import database as db
import time
import json
from flask import request

@app.get("/api/v0/user/info")
def info():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404
    res_json = {
        'status' : 'OK',
        'username' : user.username,
        'infectionTime' : user.infection_time,
        'state' : user.infection_state,
        'disease' : user.disease_name,
        'puzzles' : user.puzzles_completed,
        'roundsSurvived' : user.successful_rounds,
        'infectionCount' : user.infection_count,
        'score' : user.score,
        'role' : user.role,
        'quizRemaining' : user.quiz_remaining,
        'dnaRemaining' : user.dna_remaining,
        'xWordRemaining' : user.x_word_remaining,
        'quizRechargeTime' : user.last_quiz_recharge,
        'dnaRechargeTime' : user.last_dna_recharge,
        'crosswordRechargeTime' : user.last_x_word_recharge
    }

    return json.dumps(res_json), 200


#TODO: test if the infection end time is less than current and mark non infected
@app.get("/api/v0/user/infection/get")
def getInfection():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404
    return '{"status":"OK", "infection_status":"'+str(user.infection_state)+'", "infection_time":"'+str(user.infection_time)+'"}'

@app.post("/api/v0/user/infection/set")
def setInfection():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404

    disease = db.getCurrentDisease()[0]
    newState = request.form["state"]
    time = request.form["time"]

    user.infection_state = int(newState)
    user.infection_time = int(time)
    user.disease_name = disease
    user.infection_count += 1
    #user.infection_time = time.time()
    user.flush()
    return ""

@app.post("/api/v0/user/puzzle/add")
def addPuzzle():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404
    user.puzzles_completed += 1
    user.flush()
    return ""

@app.post("/api/v0/user/score/add")
def addScore():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404
    user.score += int(request.form["amount"])
    user.flush()
    return ""

# get scores for user and surrounding users
@app.get("/api/v0/user/scores")
def getScores():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404
    
    scores = db.getScores()
    topScores = []
    for i in range(len(scores)):
        if scores[i][1] == user.username:
            # return surrounding users
            topScores = scores[max(0, i - 2):i + 3]
            break

    res_json = [{'pos': x[0], 'user': x[1], 'score': x[2], 'image': db.getImageForUser(x[1])} for x in topScores]
    return json.dumps(res_json), 200

# scores from db are descending
@app.get("/api/v0/scores/top/get")
def getTopScores():
    scores = db.getScores()
    print(scores)
    res_json = [{'user': x[1], 'score': x[2], 'image': db.getImageForUser(x[1])} for x in scores[0:3]]
    return json.dumps(res_json), 200

@app.get("/api/v0/quiz/completed/get")
def getCompletedQuizes():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    res_json = db.getCompletedQuizzes(user.id)
    return json.dumps(res_json), 200

@app.get("/api/v0/crossword/completed/get")
def getCompletedCrosswords():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    res_json = db.getCompletedCrosswords(user.id)
    return json.dumps(res_json), 200

@app.post("/api/v0/quiz/completed/add")
def addCompletedQuiz():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    db.addQuizCompleted(user.id, request.form["quiz"])
    return '{"status":"OK"}', 200 

@app.post("/api/v0/crossword/completed/add")
def addCompletedCrossword():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    db.addCrosswordCompleted(user.id, request.form["crossword"])
    return '{"status":"OK"}', 200

@app.post("/api/v0/quiz/remaining/update")
def updateQuizRemaining():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}',404
    if (user.quiz_remaining == int(request.form['max']) or user.quiz_remaining < int(request.form['amount'])):
        user.last_quiz_recharge = time.time();
    user.quiz_remaining = int(request.form['amount'])
    user.flush()
    return ""

@app.post("/api/v0/dna/remaining/update")
def updateDnaRemaining():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    if (user.dna_remaining == int(request.form['max']) or user.dna_remaining < int(request.form['amount'])):
        user.last_dna_recharge = time.time();
    user.dna_remaining = int(request.form['amount'])
    user.flush()
    return ""

@app.post("/api/v0/xword/remaining/update")
def updateCrosswordRemaining():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    if (user.x_word_remaining == int(request.form['max']) or user.x_word_remaining < int(request.form['amount'])):
        user.last_x_word_recharge = time.time();
    user.x_word_remaining = int(request.form['amount'])
    user.flush()
    return ""
    
@app.get("/api/v0/pfp/get")
def getPFP():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    picture = db.getImageForUser(user.username)
    return '{"status":"OK", "picture":"'+picture+'"}', 200 

@app.post("/api/v0/pfp/set")
def setPFP():
    # Can't use the user object here as auth hasn't happened yet
    db.updateImageForUser(request.form["username"], request.form["image"])
    return '{"status":"OK"}', 200 

@app.get("/api/v0/user/rounds")
def getRounds():
    user = getUser()
    if (user == None):
        return '{"error":"No user"}', 404
    print(f"Successful Rounds = {user.successful_rounds}")
    return '{"status":"OK", "rounds":"'+str(user.successful_rounds)+'"}', 200

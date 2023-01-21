from singltons import app
from flask import request, make_response
import random, string, time
import database as db
ID_2_USER = {}
#TODO: make a user cleanup thread so e.g. after 10 minutes the user data is cleaned up from the active users and data is flushed to the database
class User:
    def __init__(self, Id, data):
        self.id = Id
        self.lastPoll = time.time()
        self._setdata(data)

    def _setdata(self, data):
        _, self.username, self.infection_time, self.infection_state, self.disease_name, self.puzzles_completed, self.successful_rounds, self.infection_count, self.score, self.role, self.quiz_remaining, self.dna_remaining, self.x_word_remaining, self.last_quiz_recharge, self.last_dna_recharge, self.last_x_word_recharge = data 
        
    def flush(self):
        db.setUserData(self.id, (self.username, self.infection_time, self.infection_state, self.disease_name, self.puzzles_completed, self.successful_rounds, self.infection_count, self.score, self.role, self.quiz_remaining, self.dna_remaining, self.x_word_remaining, self.last_quiz_recharge, self.last_dna_recharge, self.last_x_word_recharge))
    
    def polled(self):
        self.lastPoll = time.time()

    def resync(self):
        self._setdata(db.getUser(self.id))

def getUserObject(authId):
    data = db.getUser(authId)
    #Unable to get user with the authid
    if data == None:
        return None
    #TODO: this will interact with the database to check that the authId is valid and correct
    #Then sets up a new user object with any information needed
    return User(authId, data)

@app.post("/api/v0/user/new")
def newUser():
    if (getUser() != None):
        #note this can happen when cleanup request 262 is sent
        pass
        #return '{"error": "already logged in"}', 402
    
    if ("username" not in request.form or "uniqueifier" not in request.form):
        return '{"error": "username or uniqueifier not in payload"}', 401
    username = request.form["username"]
    unique = request.form["uniqueifier"]
    if (db.isUsernameTaken(username)):
        return '{"status":"Name Taken"}', 201
    db.createUser(unique, username)
    db.setImageForUser(username, random.choice(["pfp1.png", "pfp2.png", "pfp3.png", "pfp4.png", "pfp5.png"]))
    #TODO: create a unique token deriving from the uniqueuifier so that name can be recovered
    return '{"status":"OK", "loginToken": "'+unique+'"}', 200


@app.post("/api/v0/user/auth")
def authUser():
    resp = make_response({})
    loginAuth = request.form["authentication"]
    if (loginAuth in ID_2_USER):
        ID_2_USER[loginAuth].flush()
        resp.status_code = 200
        #if user exists need to still set session cookie
        resp.set_cookie("token", loginAuth)
        return resp
    
    user = getUserObject(loginAuth)
    if user == None:
        #resp.status_code = 401
        resp.status_code = 262
        return resp
    
    resp.set_cookie("token", user.id)
    ID_2_USER[user.id] = user
    #resp.status_code = 262
    return resp


def getUser():
    tok = request.cookies.get('token')
    if (tok == None):
        #TODO: return not authenticated error/exception
        return None
    
    if (tok in ID_2_USER):
        return ID_2_USER[tok]
    
    user = getUserObject(tok)
    if user == None:
        return None
    
    ID_2_USER[user.id] = user
    user.polled()
    return user

def syncAllUsers():
    for user in ID_2_USER.values():
        user.resync()

















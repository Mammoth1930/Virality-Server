import re
from singltons import DB_FILE
import sqlite3, time
from threading import Lock
WRITE = Lock()

dbAcc = sqlite3.connect(DB_FILE, check_same_thread=False)
dbAcc.execute('''CREATE TABLE IF NOT EXISTS USER
         (ID CHAR(50) PRIMARY KEY     NOT NULL,
         USERNAME        TEXT    NOT NULL,
         INFECTION_TIME  LONG    NOT NULL,
         INFECTION_STATE INT     NOT NULL,
         DISEASE_NAME    TEXT    NOT NULL,
         PUZZLES_COMPLETED INT   NOT NULL,
         SUCCESSFUL_ROUNDS INT   NOT NULL,
         INFECTION_COUNT INT     NOT NULL,
         SCORE           INT     NOT NULL,
         ROLE            CHAR(50),
         QUIZ_REMAINING  INT     DEFAULT 0      NOT NULL,
         DNA_REMAINING   INT     DEFAULT 0      NOT NULL,
         X_WORD_REMAINING INT    DEFAULT 0      NOT NULL,
         LAST_QUIZ_RECHARGE LONG NOT NULL,
         LAST_DNA_RECHARGE LONG  NOT NULL,
         LAST_X_WORD_RECHARGE LONG NOT NULL);''')

dbAcc.execute('''CREATE TABLE IF NOT EXISTS DISEASE
         (NAME TEXT PRIMARY KEY     NOT NULL,
         IS_CURRENT         BOOL    NOT NULL,
         VACCINE_PROGRESS   FLOAT   NOT NULL,
         CURE_NAME          TEXT    NOT NULL,
         INFECTION_PROBABILITY FLOAT NOT NULL,
         INFECTION_DURATION FLOAT   NOT NULL,
         IMMUNITY_PERIOD    FLOAT   NOT NULL,
         INFORMATION        TEXT    NOT NULL,
         COLOUR             TEXT    DEFAULT "accentOrange"  NOT NULL);''')


dbAcc.execute('''CREATE TABLE IF NOT EXISTS HISTORY
         (POS               INT     NOT NULL,
         NAME               TEXT    NOT NULL,
         VACCINE_PROGRESS   FLOAT   NOT NULL,
         COMPLETION_TIME    LONG    NOT NULL,
         NUM_INFECTIONS     INT     NOT NULL);''')

dbAcc.execute('''CREATE TABLE IF NOT EXISTS MESSAGES
            (USER           TEXT        NOT NULL,
            MESSAGE         CHAR(200)   NOT NULL,
            TIME            LONG        NOT NULL);''')

dbAcc.execute('''CREATE TABLE IF NOT EXISTS HINTS
            (DISEASE        TEXT    NOT NULL,
            HINT            TEXT    NOT NULL);''')

dbAcc.execute('''CREATE TABLE IF NOT EXISTS QUIZZESCOMPLETED
            (USER           TEXT    NOT NULL,
            QUIZ            TEXT    NOT NULL);''')

dbAcc.execute('''CREATE TABLE IF NOT EXISTS CROSSWORDSCOMPLETED
              (USER         TEXT    NOT NULL,
               CROSSWORD    TEXT    NOT NULL);''')

dbAcc.execute('''CREATE TABLE IF NOT EXISTS PFPS
            (USER            TEXT    NOT NULL,
            PICTURE         TEXT    NOT NULL);''')

dbAcc.commit()


def isUsernameTaken(username):
    cur = dbAcc.cursor()
    cur.execute('''SELECT 1 FROM USER WHERE USER.USERNAME = ?''', (username,))
    taken = cur.fetchone() != None
    cur.close()
    return taken

def getUser(token):
    cur = dbAcc.cursor()
    cur.execute('''SELECT * FROM USER WHERE USER.ID = ?''', (token,))
    userdata = cur.fetchone()
    cur.close()
    return userdata

def getUserInfectionInfo(token):
    cur = dbAcc.cursor()
    cur.execute('''SELECT INFECTION_TIME, INFECTION_STATE, USERNAME FROM USER WHERE USER.ID = ?''', (token,))
    data = cur.fetchone()
    cur.close()
    return data

def setUserInfectionState(token, state, time):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE USER SET INFECTION_STATE = ?, INFECTION_TIME = ? WHERE USER.ID = ?''', (state, time, token))
        dbAcc.commit()
        cur.close()

def setUserData(token, data):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE USER SET USERNAME=?, INFECTION_TIME=?, INFECTION_STATE=?, DISEASE_NAME=?, PUZZLES_COMPLETED=?, SUCCESSFUL_ROUNDS=?, INFECTION_COUNT=?, SCORE=?, ROLE=?, QUIZ_REMAINING=?, DNA_REMAINING=?, X_WORD_REMAINING=?, LAST_QUIZ_RECHARGE=?, LAST_DNA_RECHARGE=?, LAST_X_WORD_RECHARGE=?  WHERE USER.ID = ?''', (*data,token))
        dbAcc.commit()
        cur.close()
    
def createUser(token, username):
    with WRITE:
        cur = dbAcc.cursor()
        #Delete previous user if they had duplicate token USED FOR DEVELOPMENT/prototype, in production, create a uniqueu key
        cur.execute('''DELETE FROM USER WHERE USER.ID = ?''', (token,))
        cur.execute('''INSERT INTO USER VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (token, username, 0,0,"",0,0,0,0,"",3,3,3,time.time(),time.time(),time.time()))
        dbAcc.commit()
        cur.close()

def createDisease(name, cureName, infectionProb, duration, immunityPeriod, information, colour):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''INSERT INTO DISEASE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, False, 0, cureName, infectionProb, duration, immunityPeriod, information, colour))
        dbAcc.commit()
        cur.close()

def setCurrentDisease(name):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE DISEASE SET IS_CURRENT = 0''')
        cur.execute('''UPDATE DISEASE SET IS_CURRENT = 1 WHERE NAME = ?''', (name,))
        dbAcc.commit()
        cur.close()

def getCurrentDisease():
    cur = dbAcc.cursor()
    cur.execute('''SELECT * FROM DISEASE WHERE IS_CURRENT = 1''')
    res = cur.fetchone()
    cur.close()
    return res

def getDiseases():
    cur = dbAcc.cursor()
    cur.execute('''SELECT NAME FROM DISEASE''')
    res = cur.fetchall()
    cur.close()
    return res

def getDiseaseProgress():
    cur = dbAcc.cursor()
    cur.execute('''SELECT NAME, VACCINE_PROGRESS FROM DISEASE''')
    res = cur.fetchall()
    cur.close()
    return res

def getVacProgress(disease):
    cur = dbAcc.cursor()
    res = cur.execute('''SELECT VACCINE_PROGRESS FROM DISEASE WHERE NAME=?;''',(disease,))
    res = cur.fetchone()
    cur.close()
    return res

def addResearchProgress(name, amount):
    with WRITE:
        cur = dbAcc.cursor()
        amount = cur.execute('''SELECT VACCINE_PROGRESS FROM DISEASE WHERE NAME = ?''', (name,)).fetchone()[0] + float(amount)
        amount = min(amount, 1)
        cur.execute('''UPDATE DISEASE SET VACCINE_PROGRESS = ? WHERE NAME = ?''', (amount, name))
        dbAcc.commit()
        cur.close()

def removeResearchProgress(name):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE DISEASE SET VACCINE_PROGRESS = 0 WHERE NAME = ?''', (name,))
        dbAcc.commit()
        cur.close()

def getDiseaseColours():
    cur = dbAcc.cursor()
    cur.execute('''SELECT NAME, COLOUR FROM DISEASE''')
    res = cur.fetchall()
    cur.close()
    return res

def getMessages():
    cur = dbAcc.cursor()
    messages = cur.execute('''SELECT USER, MESSAGE FROM MESSAGES ORDER BY TIME ASC''').fetchmany(100)
    cur.close()
    return messages

def addMessage(user, message, time):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''INSERT INTO MESSAGES VALUES (?, ?, ?)''', (user, message, time))
        dbAcc.commit()
        cur.close()

def getScores():
    cur = dbAcc.cursor()
    scores = [(index + 1, values[0], values[1]) for index, values in enumerate(cur.execute('''SELECT USERNAME, SCORE FROM USER ORDER BY SCORE DESC''').fetchall())]
    cur.close()
    return scores

def getHint(disease):
    cur = dbAcc.cursor()
    hints = cur.execute('''SELECT HINT FROM HINTS WHERE DISEASE = ?''', (disease,)).fetchall()
    cur.close()
    return hints

def addHint(disease, hint):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''INSERT INTO HINTS VALUES (?, ?)''', (disease, hint))
        dbAcc.commit()
        cur.close()

def pushDiseaseStatsToHistory():
    with WRITE:
        cur = dbAcc.cursor()
        #cur.execute('''INSERT INTO HISTORY VALUES (?, ?, ?, ?, ?)''', ())
        dbAcc.commit()
        cur.close()

def resetCurrentUserDiseases():
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE USER SET INFECTION_TIME=0, INFECTION_STATE=0, DISEASE_NAME =""''')
        dbAcc.commit()
        cur.close()

def resetAllUserCrosswordsAndPuzzles():
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''DELETE FROM QUIZZESCOMPLETED WHERE 1''')
        cur.execute('''DELETE FROM CROSSWORDSCOMPLETED WHERE 1''')
        dbAcc.commit()
        cur.close()

def resetCurrentDisease():
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE DISEASE SET VACCINE_PROGRESS=0, IS_CURRENT=0 WHERE IS_CURRENT = 1''')
        dbAcc.commit()
        cur.close()

def randomlyInfectUsersOfCurrentDisease():#Infect 10% of users
    with WRITE:
        name = getCurrentDisease()[0]
        cur = dbAcc.cursor()
        cur.execute('''UPDATE USER SET INFECTION_TIME=?, INFECTION_STATE=?, DISEASE_NAME=?  WHERE ID IN (SELECT ID FROM USER ORDER BY random() LIMIT ROUND(((SELECT COUNT(*) FROM USER)*0.1)+1))''', (time.time(),1,name))
        dbAcc.commit()
        cur.close()

def getCompletedQuizzes(user):
    cur = dbAcc.cursor()
    cur.execute('''SELECT QUIZ FROM QUIZZESCOMPLETED WHERE  USER = ?''', (user,))
    res = cur.fetchall()
    cur.close()
    return res

def getCompletedCrosswords(user):
    cur = dbAcc.cursor()
    cur.execute('''SELECT CROSSWORD FROM CROSSWORDSCOMPLETED WHERE USER = ?''', (user,))
    res = cur.fetchall()
    cur.close()
    return res

def addQuizCompleted(user, quiz):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''INSERT INTO QUIZZESCOMPLETED VALUES (?, ?);''', (user, quiz))
        dbAcc.commit()
        cur.close()

def addCrosswordCompleted(user, crossword):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''INSERT INTO CROSSWORDSCOMPLETED VALUES (?, ?);''', (user, crossword))
        dbAcc.commit()
        cur.close()

def removeQuizCompleted(user, quiz):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''DELETE FROM QUIZZESCOMPLETED WHERE USER = ? AND QUIZ = ?''', (user, quiz))
        dbAcc.commit()
        cur.close()

def setImageForUser(user, image):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''INSERT INTO PFPS VALUES (?, ?)''', (user, image))
        dbAcc.commit()
        cur.close()

def getImageForUser(user):
    cur = dbAcc.cursor()
    picture = cur.execute('''SELECT PICTURE FROM PFPS WHERE USER = ?''', (user,)).fetchone()[0]
    cur.close()
    return picture

def updateImageForUser(user, image):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE PFPS SET PICTURE = ? WHERE USER = ?''', (image, user))
        dbAcc.commit()
        cur.close()

def getNumberInfected():
    cur = dbAcc.cursor()
    count = cur.execute('''SELECT COUNT(*) FROM USER WHERE INFECTION_STATE = 1''').fetchone()
    cur.close()
    return count

def addSuccessfulRounds(amount):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''UPDATE USER SET SUCCESSFUL_ROUNDS = SUCCESSFUL_ROUNDS + ?''',(amount,))
        dbAcc.commit()
        cur.close()

def deleteUser(username):
    with WRITE:
        cur = dbAcc.cursor()
        cur.execute('''DELETE FROM USER WHERE USERNAME = ?''', (username,))
        dbAcc.commit()
        cur.close()
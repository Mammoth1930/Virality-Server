from singltons import sock
from flask_sock import ConnectionClosed
from profanity import profanity
import database as db
import time
import json

# Maintain all current connections for broadcast
USERS = []

@sock.route("/api/v0/message/new/sock")
def sendMessageSock(ws):
    USERS.append(ws)
    for (user, message) in db.getMessages():
        ws.send(json.dumps({"user": user, "message": message}))
    while True:
        try:
            message = ws.receive()
        except ConnectionClosed:
            if user in USERS:
                USERS.remove(user)
            break
        
        data = json.loads(message)
        data["message"] = profanity.censor(data["message"])
        updatedMessage = json.dumps(data)
        
        db.addMessage(data["user"], data["message"], int(time.time()))

        for user in USERS:
            try:
                user.send(updatedMessage)
            except ConnectionClosed:
                pass

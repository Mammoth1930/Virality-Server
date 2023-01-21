from singltons import app
from flask import request, make_response,send_from_directory,render_template
import database

@app.get('/admin/dday/access')
def setup_access():
    response = make_response()
    response.location = "/admin/dday/main"
    response.set_cookie("AccessAuthed", "yes i have access")
    response.status_code = 302
    return response

@app.get('/admin/dday/main')
def send_dday_landing():
    if "AccessAuthed" not in request.cookies:
        return "", 418
    if request.cookies["AccessAuthed"] != "yes i have access":
        return "", 418
        
    return render_template("main.html", testtt = "hello")


a = 0
@app.get('/admin/dday/stats')
def send_dday_stats():
    if "AccessAuthed" not in request.cookies:
        return "", 418
    if request.cookies["AccessAuthed"] != "yes i have access":
        return "", 418
    global a
    a+=1   
    return render_template("statistics.html", infectionCount = str(database.getNumberInfected()[0]), 
    vaccineProgress = [(name, int(progress * 100)) for name, progress in database.getDiseaseProgress()],
    leaderboard = database.getScores()[:10]
    )

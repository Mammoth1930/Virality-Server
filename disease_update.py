import database, random, authentication
import threading, time, datetime
from dateutil.relativedelta import relativedelta,SU,MO

def getTimeTillNextEvent():
    dt = datetime.datetime.now()
    nextWeek = dt + relativedelta(weekday=SU(+1), hour=23, minute = 59, second = 59)
    delta = nextWeek - dt
    return delta.total_seconds()
    
def weekly_tick():
    while True:
        tte = getTimeTillNextEvent()
        print("Time till event end:",tte)
        time.sleep(tte)
        print("Event over")
        for i in authentication.ID_2_USER.values():
            i.flush()
        cdisease = database.getCurrentDisease()[0]
        if (cdisease == None):
            print("No current event")
            continue
        database.pushDiseaseStatsToHistory()
        database.resetCurrentUserDiseases()
        database.resetAllUserCrosswordsAndPuzzles()
        database.resetCurrentDisease()
        diseases = list(map(lambda x:x[0], database.getDiseases()))
        diseases.remove(cdisease)
        newDisease = random.choice(diseases)
        database.setCurrentDisease(newDisease)
        database.randomlyInfectUsersOfCurrentDisease()
        authentication.syncAllUsers()
if "looper" not in globals():
    looper = threading.Thread(target=weekly_tick)
    looper.setDaemon(True)
    looper.start()
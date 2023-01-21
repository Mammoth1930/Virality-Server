from singltons import app
import os
app.debug = True
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    import api
    import disease_update
    import dday.server
    



if (__name__=="__main__"):
    app.run(host="0.0.0.0", port = 80)

# Getting Started

## Running it locally

Run `sudo pip install -r requirements.txt`  
Run `sudo python3 main.py`  
To connect to it with the app, you will need to change the endpoint in `lib/api/UserAPI.dart` in the viral_gamification_app code to the one that is commented out. It should contain the IP 10.0.2.2.
When main.db is created for the first time, you will need to initialise some data. Substitute the host and port for what the python output gives when you run the server:  
`curl http://127.0.0.1/api/v0/admin/disease/test`  
`curl http://127.0.0.1/api/v0/admin/hints/add`  

## Running it on the server

The server is hosted on uqzone, to access it log into moss.labs.eait.uq.edu.au then ssh into deco3801-teamexe.zones.eait.uq.edu.au while on moss.

The code is auto pulled via a CI on tmux session 0, this shouldent crash and will always pull the latest commits from main into it

The server itself is running in a tmux session called server, to access this type `tmux attach -d -t server` on the uq zone server, this will bring up the server itself, any errors and api accesses will be shown here. UPDATE - the tmux session appears to only be accessible by the user who created it

If you pushed a change to the database schema you will need to reset the database. To do this first kill the server with ctrl+c, then type `sudo rm main.db` to delete the database file then restart the server as follows.

If the server goes down for some unexplained error, issue or other, too relaunch it, make sure you are in the 
`/home/project/viral_gamification_server` directory then run `sudo python3 main.py` to relaunch the server

To detach from the tmux instance `ctrl+b` then `d` do not do `ctrl+d` as this will terminate the tmux session,
if you accidently kill the session, create a new session with the command `tmux new -s server` and restart the server


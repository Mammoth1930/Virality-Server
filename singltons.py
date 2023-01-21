from flask import Flask
from flask_sock import Sock
app = Flask(__name__)
sock = Sock(app)
DB_FILE = "main.db"

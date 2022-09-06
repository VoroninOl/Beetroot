from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
# import app.pyfiles.config as cfg


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

app.config['DEBUG'] = True

db = SQLAlchemy(app)

socketio = SocketIO(app)

from app.pyfiles import routes

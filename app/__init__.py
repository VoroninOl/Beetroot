from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from app.pyfiles.config import secret


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/messages.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret


db = SQLAlchemy(app)

socketio = SocketIO(app)

from app.pyfiles import routes

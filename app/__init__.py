from flask import Flask
from flask_socketio import SocketIO
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# import app.pyfiles.config as cfg


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

app.config['DEBUG'] = True

socketio = SocketIO(app)

# login_manager = LoginManager(app)
# db = SQLAlchemy(app)

from app.pyfiles import routes

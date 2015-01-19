import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os

#print os.getcwd()
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s/data.db'%os.getcwd()
app.secret_key = 'thisisarandomstring007becauseilovejamesbond'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
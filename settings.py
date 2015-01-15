import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////vagrant/projects/lonelyIsland/data.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
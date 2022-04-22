from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

Session(app)
db = SQLAlchemy(app)
moment = Moment(app)

from . import routes

import flask_login
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_caching import Cache
from flask_login import LoginManager


db = SQLAlchemy()
api = Api()
cache = Cache()
login_manager = LoginManager()

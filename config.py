from os import  environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Base:
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    FLASK_APP = environ.get('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
class Product(Base):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PRODUCT_DATABASE_URI')
    SQLALCHEMY_ECHO = False

class Dev(Base):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_ECHO = True

class SMS:
    APPID = environ.get('SMS_APPID')
    APPKEY = environ.get('SMS_APPKEY')

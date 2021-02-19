from os import  environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Base:
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    #FLASK_APP = 'sophia'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
  
class Dev(Base):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True

class SMS:
    APPID = environ.get('SMS_APPID')
    APPKEY = environ.get('SMS_APPKEY')

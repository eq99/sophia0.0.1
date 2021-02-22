from os import  environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Production:
    '''
    Our config is production first, so we can do CI/CD easily.
    - DATABASE_URI: Because we don't publish `.env` file, `DATABASE_URI`
    is different between dev computer and production computer.
    '''
    SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
  
class Dev(Production):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True

from flask import Flask
from plugins import db, cache, login_manager
from app.models import User
from app.home import home
from app.course import (
    course_bp,
    course,
    chapter,
    new_course
)

from app.user import (
   user_bp
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Dev')

    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)


    app.add_url_rule('/', 'home', home)
    # app.add_url_rule('/smscode', 'smscode', smscode, methods=['GET','POST'])
    # app.add_url_rule('/signin', 'signin', signin, methods=['GET', 'POST'])
    # app.add_url_rule('/course/<course_name>', 'course', course)
    # app.add_url_rule('/course/new', 'new_course', new_course, methods=['GET', 'POST'])
    # app.add_url_rule('/course/<course_name>/chapter/<chapter_name>', 'chapter', chapter)

    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)

    return app
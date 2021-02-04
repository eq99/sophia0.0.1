from flask import Flask
from plugins import db
from app.home import home
from app.course import (
    course,
    chapter,
    new_course
)

from app.user import (
    signin
)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Dev')

    db.init_app(app=app)

    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/signin', 'signin', signin)
    app.add_url_rule('/course/<course_name>', 'course', course)
    app.add_url_rule('/course/new', 'new_course', new_course)
    app.add_url_rule('/course/<course_name>/chapter/<chapter_name>', 'chapter', chapter)

    return app
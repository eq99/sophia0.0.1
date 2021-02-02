from flask import Flask
from plugins import db
from app.course.view import course_bp

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Dev')

    db.init_app(app=app)

    blueprints=[course_bp]
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
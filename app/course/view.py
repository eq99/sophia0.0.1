from flask import Blueprint

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/')
def home():
    return 'hello world!'
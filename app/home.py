from flask import (
    render_template
)

from app.models import Course

def home():
    courses_raw = Course.query.all()
    courses=[]
    for course_raw in courses_raw:
        courses.append({
            'name': course_raw.name,
            'url': f'/course/{course_raw.name}',
            'description': course_raw.description
        })
    return render_template(
        'home.html',
        courses=courses
        )
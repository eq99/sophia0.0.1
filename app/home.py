from flask import (
    render_template
)

from flask_login import current_user

from app.models import Course

def home():
    courses = Course.query.all()
    # courses=[]
    # for course_raw in courses_raw:
    #     courses.append({
    #         'name': course_raw.name,
    #         'url': f'/course/{course_raw.id}',
    #         'description': course_raw.description,
    #         'cover_url': course_raw.cover_url
    #     })
    return render_template(
        'home.html',
        title='Book list',
        courses=courses,
        is_admin=hasattr(current_user, 'id') and (current_user.id==8)
        )
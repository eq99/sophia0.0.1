from flask import(
    render_template
)

def course(course_name):
    return render_template('course.html')

def new_course():
    return render_template('new_course.html')

def chapter(course_name, chapter_name):
    return render_template('chapter.html')

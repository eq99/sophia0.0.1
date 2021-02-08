from datetime import datetime

from flask import(
    Blueprint,
    render_template,
    request,
    flash
)

from flask_login import(
    current_user
)
from werkzeug.utils import redirect

from plugins import(
    db
)

from app.models import(
    Course,
    User,
    Chapter,
    Version
)

course_bp = Blueprint('course_bp', __name__, url_prefix='/course')

@course_bp.route('/<course_name>')
def course(course_name):
    course = Course.query.filter(Course.name == course_name).first()
    chapters_raw = Chapter.query.filter(Chapter.course_id == course.id).all()
    chapters=[]
    for chapter_raw in chapters_raw:
        chapter={
            'name': chapter_raw.name,
            'notes': chapter_raw.notes,
            'url': f'/course/{course_name}/chapter/{chapter_raw.name}',
            'new_chapter': f'/course/{course_name}/chapter/{chapter_raw.name}/new'
        }
        chapters.append(chapter)
    return render_template(
        'course.html',
        course_name=course_name,
        chapters=chapters
        )

@course_bp.route('/new', methods=['GET', 'POST'])
def new_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description')
        course = Course.query.filter(Course.name == course_name).first()
        user = User.query.filter(User.id == current_user.id).all()
        print(user)
        if course is None:
            latest_version = Version(
                contributor_id=current_user.id,
                description='create course.',
                created_time=datetime.now(),
                is_accepted=True,
                content='Write Introduction here.'
            )

            first_chapter = Chapter(
                name='Introduction',
                notes='Your first glance.',
                created_time=datetime.now(),
                updated_time=datetime.now(),
                latest_version=latest_version
            )

            course = Course(
                name=course_name,
                description=course_description,
                managers=user, # require list
                created_time=datetime.now(),
                first_chapter=first_chapter
            )
            db.session.add(course)
            db.session.commit()


            flash(f'Create course {course_name} Success.')
        else:
            flash(f'{course_name} aready exist.')

        return redirect(f'/course/{course_name}')
    else:
        return render_template('new_course.html')

@course_bp.route('/<course_name>/chapter/<chapter_name>')
def chapter(course_name, chapter_name):
    course = Course.query.filter(Course.name==course_name).first()
    chapter = Chapter.query.filter(db.and_(Chapter.course_id==course.id, Chapter.name==chapter_name)).first()
    print(f'chapter:{chapter}')
    return render_template(
        'chapter.html',
        chapter=chapter
        )

@course_bp.route('/<course_name>/chapter/<chapter_name>/new', methods=['GET', 'POST'])
def new_chapter(course_name, chapter_name):
    if request.method == 'POST':
        new_chapter_name = request.form.get('chapter_name')
        new_chapter_notes = request.form.get('chapter_notes')
        new_chapter_content = request.form.get('chapter_content')
        course = Course.query.filter(Course.name == course_name).first()
        current_chapter = Chapter.query.filter(db.and_(Chapter.course_id==course.id, Chapter.name==chapter_name)).first()
        if new_chapter_name == current_chapter.name:
            return redirect('/course/<course_name>/chapter/<chapter_name>')

        latest_version = Version(
            contributor_id=current_user.id,
            description=f'create chapter {new_chapter_name}.',
            created_time=datetime.now(),
            is_accepted=True,
            content=new_chapter_content
        )

        new_chapter = Chapter(
            name=new_chapter_name,
            notes=new_chapter_notes,
            created_time=datetime.now(),
            updated_time=datetime.now(),
            latest_version=latest_version,
            previous_chapter_id=current_chapter.id,
            course_id=course.id
        )
        db.session.add(new_chapter)
        db.session.commit()

        return redirect(f'/course/{course_name}/chapter/{new_chapter_name}')

        
    else:
        return render_template(
            'new_chapter.html',
            action_url=f'/course/{course_name}/chapter/{chapter_name}/new'
        )
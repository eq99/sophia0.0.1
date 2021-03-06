from datetime import datetime
from difflib import unified_diff
import re
from os import environ
from flask import(
    Blueprint,
    render_template,
    redirect,
    request,
    flash,
    jsonify
)

from flask_login import(
    current_user,
    login_required
)

from sts.sts import Sts

from plugins import(
    db
)

from app.models import(
    Course,
    User,
    Chapter,
    Version,
)

course_bp = Blueprint('course_bp', __name__,template_folder='./templates/course')


@course_bp.route('/course/<course_id>')
def course(course_id):
    '''
    The home page of course with id.
    Args:
      course_id: Integer
        id of the course in the database.

    Returns:
      course.html:
        - show chapter list.
        - add/delete a new chapter.
    '''

    course = Course.query.get(course_id)
    current_chapter = course.first_chapter
    # chapters_raw = Chapter.query.filter(Chapter.course_id == course_id).all()
    chapters=[]
    while current_chapter:
        chapters.append({
            'name': current_chapter.name,
            'notes': current_chapter.notes,
            'id': current_chapter.id,
            # 'url': f'/course/{course_Vid}/chapter/{current_chapter.id}',
            # 'new_chapter_url': f'/course/{course_id}/chapter/{current_chapter.id}/new',
            # 'pull_requests_url': f'/course/{course_id}/chapter/{current_chapter.id}/prs',
            # 'edit_name_url': f'/course/{course_id}/chapter/{current_chapter.id}/edit'
        })
        current_chapter = current_chapter.next_chapter
    # for chapter_raw in chapters_raw:
    #     chapters.append({
    #         'name': chapter_raw.name,
    #         'notes': chapter_raw.notes,
    #         'url': f'/course/{course_id}/chapter/{chapter_raw.id}',
    #         'new_chapter_url': f'/course/{course_id}/chapter/{chapter_raw.id}/new',
    #         'pull_requests_url': f'/course/{course_id}/chapter/{chapter_raw.id}/prs',
    #         'edit_name_url': f'/course/{course_id}/chapter/{chapter_raw.id}/edit'
    #     })
    return render_template(
        'course.html',
        title=course.name,
        course_id = course_id,
        chapters=chapters
        )


@course_bp.route('/sts')
def sts():
    '''
    `sts` service for temporary secret
    See https://cloud.tencent.com/document/product/436/11459#.E8.8E.B7.E5.8F.96.E4.B8.B4.E6.97.B6.E5.AF.86.E9.92.A5
    '''
    config = {
        'url': 'https://sts.tencentcloudapi.com/',
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': environ.get('COS_SECRET_ID'),
        # 固定密钥
        'secret_key': environ.get('COS_SECRET_KEY'),
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': environ.get('COS_BUCKET_NAME'),
        # 换成 bucket 所在地区
        'region': environ.get('COS_BUCKET_REGION'),
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            'name/cos:PutObject',
            'name/cos:PostObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload'
        ],

    }

    try:
        sts = Sts(config)
        return sts.get_credential()
    except Exception as e:
        return jsonify(
            message="error",
            error=e
        )

@course_bp.route('/course/new', methods=['GET', 'POST'])
def new_course():
    '''
    Create a new course. Requires:
      - `course_name` is unique in the database.
      - When a new course is created, the default chapter
        `Introduction` with a default version is created.
    Returns:
      - new_course.html: Including forms to collect new course infos.
      - redirect to course.html when there is course with `course_name`
    '''

    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description')
        course = Course.query.filter(Course.name == course_name).first()
        user = User.query.filter(User.id == current_user.id).all()
        if course is None:
            first_version = Version(
                contributor_id=current_user.id,
                description='create course.',
                created_time=datetime.now(),
                status='ACCEPTED',
                content='Write your Introduction here.'
            )

            db.session.add(first_version)
            db.session.flush()
            db.session.refresh(first_version)
            
            first_chapter = Chapter(
                name='Introduction',
                notes=f'Get started with {course_name}',
                created_time=datetime.now(),
                updated_time=datetime.now(),
                latest_version_id=first_version.id
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

            # get course id for the new course
            course = Course.query.filter(Course.name == course_name).first()
            return redirect(f'/course/{course.id}')
        else:
            flash(f'{course_name} aready exist.')
            return redirect(f'/course/{course.id}')
    else:
        return render_template('new_course.html')

@course_bp.route('/course/<course_id>/manage')
def manage_course(course_id):
    if request.method == 'POST':
        pass
    else:
        course = Course.query.get(course_id)
        return render_template(
            'manage_course.html',
            title="manage course",
            course=course
            )

@course_bp.route('/course/<course_id>/chapter/<chapter_id>')
def chapter(course_id, chapter_id):
    '''
    Show details about a chapter.
    Arges:
      chapter_id: id of a chapter in the database
    Returns:
      chapter.html:
        - name of chapter, aka the article title.
        - content of the chapter.
        - history of the chapter.
        - edit the chapter
    '''
    chapter = Chapter.query.get(chapter_id)
    latest_version = Version.query.get(chapter.latest_version_id)
    return render_template(
        'chapter.html',
        title=chapter.name,
        course_id = course_id,
        chapter_id = chapter_id,
        content = latest_version.content
        )


@course_bp.route('/course/<course_id>/chapter/<chapter_id>/manage', methods=['GET','POST'])
@login_required
def chapter_manage(course_id, chapter_id):
    if request.method == 'POST':
        chapter_name = request.form.get('chapter_name')
        chapter_notes = request.form.get('chapter_notes')
        edit_description = request.form.get('edit_description')
        edit_content = request.form.get('edit_content')
        
        chapter = Chapter.query.get(chapter_id)
        if chapter_name:
            chapter.name = chapter_name
        
        if chapter_notes:
            chapter.notes = chapter_notes
        
        version = Version(
            contributor_id = current_user.id,
            description = edit_description,
            created_time = datetime.now(),
            status = 'ACCEPTED',
            content = edit_content,
            previous_version_id = chapter.latest_version.id,
            chapter_id = chapter_id,
            course_id = course_id
        )

        db.session.add(version)
        db.session.flush()
        db.session.refresh(version)
        chapter.latest_version_id = version.id
        db.session.commit()


        return jsonify(
            message=f'{chapter_name} update success.'
        )

    else:
        chapter = Chapter.query.get(chapter_id)
        return render_template(
            'chapter_manage.html',
            title = '章节管理',
            course_id = course_id,
            chapter = chapter
        )

@course_bp.route('/course/<course_id>/chapter/<chapter_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_chapter(course_id, chapter_id):
    '''
    Change name or content about a chapter.
    The changes will be posted to Stage.
    '''
    chapter = Chapter.query.get(chapter_id)
    if request.method == 'POST':
        content = request.form.get('edit_content')
        description = request.form.get('edit_description')
        version = Version(
            description=description or '做了一些修改',
            created_time=datetime.now(),
            content=content,
            status='OPEN',
            chapter_id=chapter.id,
            course_id=course_id
        )
        user = User.query.get(current_user.id)
        user.contributes.append(version)
        db.session.add(version)
        db.session.commit()
        return jsonify(
            message="提交成功",
            chapter_url=f'/course/{course_id}/chapter/{chapter_id}'
        )
    else:
        return render_template(
            'edit_chapter.html',
            title='Edit',
            contents_url=f'/course/{course_id}',
            edit_action_url=f'/course/{course_id}/chapter/{chapter_id}/edit',
            chapter=chapter
        )
       
def get_diff(old_content:str, new_content:str):
    return '<br>'.join(list(unified_diff(old_content.splitlines(True), new_content.splitlines(True), fromfile='old', tofile='new', lineterm='')))

@course_bp.route('/course/<course_id>/chapter/<chapter_id>/prs')
def pull_requests(course_id, chapter_id):
    '''
    Contributor's change will list here.
    '''
    versions = Version.query.filter(db.and_(Version.chapter_id==chapter_id, Version.status=='OPEN'))
    latest_version_id = Chapter.query.get(chapter_id).latest_version_id
    latest_version = Version.query.get(latest_version_id)
    prs=[]
    for version in versions:
        prs.append({
            'accept_url': f'/course/{course_id}/chapter/{chapter_id}/prs/{version.id}/accept',
            'reject_url': f'/course/{course_id}/chapter/{chapter_id}/prs/{version.id}/reject',
            'contributor': version.contributor,
            'created_time': version.created_time.strftime("%Y %m %d %H:%M:%S"),
            'description': version.description,
            'diff': get_diff(latest_version.content, version.content)
        })
    return render_template(
        'pull_requests.html',
        titel='Pull Requests',
        contents_url=f'/course/{course_id}',
        prs=prs
    )

@course_bp.route('/course/<course_id>/chapter/<chapter_id>/prs/<version_id>/accept')
def accept_version(course_id, chapter_id, version_id):
    version = Version.query.get(version_id)
    chapter = Chapter.query.get(chapter_id)
    version.previous_version_id = chapter.latest_version_id
    version.status = 'ACCEPTED'
    chapter.latest_version_id = version.id
    db.session.commit()
    return redirect(f'/course/{course_id}/chapter/{chapter_id}/prs')


@course_bp.route('/course/<course_id>/chapter/<chapter_id>/prs/<version_id>/reject')
def reject_version(course_id, chapter_id, version_id):
    version = Version.query.get(version_id)
    version.status='REJECTED'
    db.session.commit()
    return redirect(f'/course/{course_id}/chapter/{chapter_id}/prs')

@course_bp.route('/course/<course_id>/chapter/<chapter_id>/new', methods=['GET', 'POST'])
def new_chapter(course_id, chapter_id):
    '''
    Create a new succeeding chapter for current chapter.
    Arges:
      course_id: new chapter blongs to this course
      chapter_id: current chapter, a new chapter will be created next to it.
    Returns:
      new_chapter.html: Including forms to collect the new chapter infos.
      chapter.html: Will redirect this if the chapter_name already exists or created the new chapter.
    '''
    if request.method == 'POST':
        new_chapter_name = request.form.get('chapter_name')
        new_chapter_notes = request.form.get('chapter_notes')
        new_chapter_content = request.form.get('chapter_content')
        print(f'chapter content: {new_chapter_content}')
        course = Course.query.get(course_id)
        current_chapter = Chapter.query.get(chapter_id)

        # Note: chapter name in a course is unique, but not unique in database.
        chapter_with_name = Chapter.query.filter(db.and_(Chapter.course_id==course_id, Chapter.name==new_chapter_name))
        if new_chapter_name == chapter_with_name:
            return redirect(f'/course/{course_id}/chapter/{chapter_with_name.id}')

        # When a new chapter is created, a default verion of it will alse be created.
        latest_version = Version(
            contributor_id=current_user.id,
            description=f'create chapter {new_chapter_name}.',
            created_time=datetime.now(),
            status='ACCEPTED',
            content=new_chapter_content
        )
        db.session.add(latest_version)
        db.session.flush()
        db.session.refresh(latest_version)

        new_chapter = Chapter(
            name=new_chapter_name,
            notes=new_chapter_notes,
            created_time=datetime.now(),
            updated_time=datetime.now(),
            latest_version_id=latest_version.id,
            next_chapter=current_chapter.next_chapter,
            course_id=course.id
        )
        current_chapter.next_chapter = new_chapter
        db.session.add(new_chapter)
        db.session.commit()
        # get id of the new chapter
        # new_chapter = Chapter.query.filter(Chapter.name == new_chapter_name).first()
        # we use `new_chapter_url` for `window.location.href` to redirect after ajax
        # see: https://stackoverflow.com/questions/47122295/flask-how-to-redirect-to-new-page-after-ajax-call
        return jsonify(
            code=200,
            new_chapter_url=f'/course/{course_id}'
        )

    else:
        return render_template(
            'new_chapter.html',
            new_chapter_url=f'/course/{course_id}/chapter/{chapter_id}/new'
        )


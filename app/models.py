from plugins import db

course_managers = db.Table('course_managers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('is_present', db.Boolean)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True, nullable=False)
    avatar_url = db.Column(db.String)
    school = db.Column(db.String)
    phone = db.Column(db.String(11), index=True, unique=True, nullable=False)
    token = db.Column(db.String)
    managed_courses = db.relationship('Course', secondary=course_managers, back_populates='managers')
    contributes = db.relationship('Version', back_populates='contributor')


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contributor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contributor = db.relationship('User', back_populates='contributes')
    description = db.Column(db.String)
    created_time = db.Column(db.DateTime)
    is_accepted = db.Column(db.Boolean, default=False)
    content = db.Model(db.Text)
    previous_version = db.Column(db.Integer, db.ForeignKey('version.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    chapter = db.relationship('Chapter', back_populates='latest_version')


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)
    latest_version = db.relationship('Version', back_poulates='chapter', uselist=False)
    previous_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    next_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    course_id = db.Column(db.Integer)
    course = db.relationship('Course', back_populates='first_chapter')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String, unique=True, nullable=False)
    managers = db.relationship('User', secondary=course_managers, back_populates='managed_courses')
    description = db.Column(db.String)
    cover_url = db.Column(db.String)
    created_time = db.Column(db.DateTime)
    first_chapter = db.relationship('Chapter', back_populates='course', uselist=False)

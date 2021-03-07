from enum import Enum
from sqlalchemy.orm import backref, defaultload
from plugins import db
from flask_login import UserMixin


# class CourseManager(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
#     is_present =  db.Column(db.Boolean)

# course_managers = db.Table('course_managers',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
#     db.Column('is_present', db.Boolean)
# )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True, nullable=False)
    avatar_url = db.Column(db.String)
    gender = db.Column(db.Boolean, default=False) # True: male; Flase: female
    reputation = db.Column(db.Float, default=0.0)
    school = db.Column(db.String)
    phone = db.Column(db.String(11), index=True, unique=True, nullable=False)

    # this field can also be used as `role`
    status = db.Column(db.String) # 'NORMAL', 'ADMIN', 'FREEZE'
    
    created_time = db.Column(db.DateTime)
    # managed_courses = db.relationship('Course', secondary=course_managers, back_populates='managers')
    contributes = db.relationship('Version', backref='contributor')

    def is_active(self):
        return self.is_active

    # def is_anonymous(self):
    #     return False

    # def is_authenticated(self):
    #     return True
    
    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f'User< {self.id} {self.nickname}>'

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contributor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String)
    created_time = db.Column(db.DateTime)

    status = db.Column(db.String) # 'OPEN', 'ACCEPTED', 'REJECTED'
    # 'OPEN': when a new changed is created
    # 'ACCEPTED': change is accepted by course manager
    # 'REJECTED': change is rejected by course manager
    content = db.Column(db.Text)
    previous_version_id = db.Column(db.Integer, db.ForeignKey('version.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self) -> str:
        return f'<Version {self.created_time}>'


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    notes = db.Column(db.String)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)
    latest_version_id = db.Column(db.Integer, db.ForeignKey('version.id'))

    # The following two fields defines the chapter order
    # see https://docs.sqlalchemy.org/en/14/orm/self_referential.html
    previous_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    next_chapter = db.relationship('Chapter', uselist=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', back_populates='first_chapter') # dumbfl

    def __repr__(self) -> str:
        return f'<Chapter {self.name}>'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    # managers = db.relationship('User', secondary=course_managers, back_populates='managed_courses')
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String)
    cover_url = db.Column(db.String)
    created_time = db.Column(db.DateTime)
    first_chapter = db.relationship('Chapter', back_populates='course', uselist=False)

    def __repr__(self) -> str:
        return f'<Course {self.name}>'

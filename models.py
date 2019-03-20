import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('ta.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    course = CharField(default="General")
    avatar = CharField(default="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
    role = CharField(default="Student")
    
    class Meta:
        database = DATABASE

    def get_events(self):
        return Event.select().where(Event.user == self)
        
    @classmethod
    def create_user(cls, username, email, password, avatar="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png", course="General", role="Student"):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                course=course,
                avatar=avatar,
                role=role
            )
        except IntegrityError:
            raise ValueError("User already exists")

class Event(Model):
    student = ForeignKeyField(
        model=User,
        backref='events'
    )
    instructor = ForeignKeyField(
        model=User,
        backref='events'
    )
    title = CharField(max_length=256, default="I am a title")
    notes = CharField(max_length=256, default="Bleep Bloop")

    class Meta:
        database = DATABASE

    @classmethod
    def create_event(cls, student, instructor, title, notes):
        try:
            cls.create(
                student=student,
                instructor=instructor,
                title=title,
                notes=notes
            )
        except IntegerError:
            raise ValueError("Something broke")
        
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Event], safe=True)
    DATABASE.close()
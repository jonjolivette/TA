import datetime
from peewee import *
import moment

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('ta.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    role = CharField()
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    course = CharField(default="General")
    avatar = CharField(default="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png")

    class Meta:
        database = DATABASE

    def get_events(self):
        return Event.select().where(Event.user == self)

    @classmethod
    def create_user(cls, username, email, role, password, avatar="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png", course="General"):
        try:
            cls.create(
                username=username,
                email=email,
                role=role,
                password=generate_password_hash(password),
                course=course,
                avatar=avatar
            )
        except IntegrityError:
            raise ValueError("User already exists")


class Event(Model):
    student = ForeignKeyField(
    model=User,
    backref='events',
    null=True
    )
    instructor = ForeignKeyField(
    model=User,
    backref='events'
    )
    date = DateField()
    duration = CharField()
    notes = CharField(max_length=256, default="Bleep Bloop")

    class Meta:
        database = DATABASE

    @classmethod
    def create_event(cls, instructor, duration, date):
        try:
            cls.create(
                instructor=instructor,
                date=date,
                duration=duration
            )
        except IntegrityError:
            raise

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Event], safe=True)
    DATABASE.close()


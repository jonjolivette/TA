from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(512))
    course = db.Column(db.String(128), nullable=False)

    # repr changes the way print represents text so we can just pass information through a custom message
    def __repr__(self):
        return (f'<User is {self.user}>')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)
    # student = foreign key to user db
    # instructor = foreign key to user db
    title = db.Column(db.String(256))
    notes = db.Column(db.String(512))




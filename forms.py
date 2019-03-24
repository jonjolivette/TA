from flask_wtf import FlaskForm as Form

from models import User
import datetime
import moment
import time

from wtforms import StringField, PasswordField, TextAreaField, SelectField, TimeField

from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    username = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    # role = SelectField(
    #     'role',
    #     choices=[("Student","Student"), ("Instructor","Instructor")],
    #     default="Student"
    # )
    course = SelectField(
        'Course',
        choices=[("General", 'General'), ("WDI 51", 'WDI 51'), ("WDI 52", 'WDI 52')],
        default="General"
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )

# class DeleteUserForm(Form):


class CreateEventForm(Form):
    date = DateField(
        'Date',
        default=moment.utcnow(),
        validators=[
            DataRequired()
        ],
    )
    time = SelectField(
        'Time',
        choices=[("4:00 PM", '4:00 PM'), ("4:15 PM", '4:15 PM'), ("4:30 PM", '4:30 PM'), ("4:45 PM", '4:45 PM'), ("5:00 PM", '5:00 PM')],
    )

class EditEventForm(Form):
    date = DateField(
        'Date',
        default=moment.utcnow(),
        validators=[
            DataRequired()
        ],
    )
    time = SelectField(
        'Time',
        choices=[("4:00 PM", '4:00 PM'), ("4:15 PM", '4:15 PM'), ("4:30 PM", '4:30 PM'), ("4:45 PM", '4:45 PM'), ("5:00 PM", '5:00 PM')],
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

# class PostForm(Form):
#     content = TextAreaField("Enter Post here", validators=[DataRequired()])

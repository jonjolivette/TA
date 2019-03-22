from flask_wtf import FlaskForm as Form

from models import User

from wtforms import StringField, PasswordField, TextAreaField, DateField, SelectField
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
    role = SelectField(
        'role',
        choices=[("Student","Student"), ("Instructor","Instructor")],
        default="Student"
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
        validators=[
            DataRequired()
        ],
        format="%Y-%m-%d"
    )
    duration = SelectField(
        'Duration',
        choices=[("15", '15 Minutes'), ("30", '30 Minutes'), ("45", '45 Minutes')],
        default="15"
    )

class EditEventForm(Form):
    date = DateField(
        'Date',
        validators=[
            DataRequired()
        ],
        format="%Y-%m-%d"
    )
    duration = SelectField(
        'Duration',
        choices=[("15", '15 Minutes'), ("30", '30 Minutes'), ("45", '45 Minutes')],
        default="15"
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

# class PostForm(Form):
#     content = TextAreaField("Enter Post here", validators=[DataRequired()])

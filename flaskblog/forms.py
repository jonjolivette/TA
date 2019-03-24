from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    # means data is required and the min and max for it
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
# These two methods below validate the reg form 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).all()
        if user:
            raise ValidationError('That username is taken. please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).all()
        if user:
            raise ValidationError('That email is taken. please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    # means data is required and the min and max for it
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Allows the following extensions to be uploaded as photos
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
# These two methods below validate the updateAccount form not allowing an existent account to be created
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).all()
            if user:
                raise ValidationError('That username is taken. please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).all()
            if user:
                raise ValidationError('That email is taken. please choose a different one')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
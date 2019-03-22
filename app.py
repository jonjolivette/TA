# from flask import render_template
from flask import Flask, g
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from config import Config

import moment

import models
from models import User
from models import Event
import forms

DEBUG = True
PORT = 8000


app = Flask(__name__)
app.config.from_object(Config)


login_manager = LoginManager()
# sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

# Connect to database before request
@app.before_request
def before_request():
    """Connect to database before each request """
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

# ============ REGISTRATION PAGE ROUTE ============
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Hooray, you registered!", 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            password=form.password.data
        )

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# ============ LOGIN PAGE ROUTE ============
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                # creates session
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)


# ============ LOGOUT PAGE ROUTE ============

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))

# ============ EVENT CREATE ROUTE ============


@app.route('/event/create', methods=('GET', 'POST'))
# @login_required
def create_event():
    form = forms.CreateEventForm()
    if g.user.role != "Instructor":
        return redirect(url_for('index'))

    if form.validate_on_submit():
        flash("Hooray, you registered!", 'success')
        models.Event.create_event(
            instructor=g.user.id,
            date=form.date.data,
            duration=form.duration.data,
        )

        # return redirect(url_for('index'))
    return render_template('create_event.html', form=form)

# ============ EVENT PAGE ROUTE ============


@app.route('/event',  methods=('GET', 'POST'))
@login_required
def event():
    events = Event.select()
    return render_template('event.html', events=events)


@app.route('/event/delete/<id>', methods=['DELETE', 'GET'])
@login_required
def event_delete(id):
    found_event = Event.select().where(Event.id == id)
    if g.user.id == found_event[0].instructor_id:
        event_to_delete = Event.delete().where(Event.id == found_event[0].id)
        event_to_delete.execute()
    return redirect(url_for('event'))


@app.route('/event/update/<id>', methods=('POST', 'GET'))
def event_update(id):
    form = forms.EditEventForm()
    found_event = Event.select().where(Event.id == id)
    if g.user.id == found_event[0].instructor_id:
        if form.validate_on_submit():
            update = Event.update(
                duration=form.duration.data, date=form.date.data).where(Event.id == id)
            update.execute()
            return redirect(url_for('event'))

    return render_template('edit_event.html', form=form, found_event=found_event[0])


@app.route('/event/add_student/<id>', methods=('POST', 'GET'))
def add_student_to_event(id):
    found_event = Event.select().where(Event.id == id)
    if found_event[0].student == None:
        add_student = Event.update(
            student=current_user.id).where(Event.id == id)
        add_student.execute()
    return redirect(url_for('event'))


# ============ HOME PAGE ROUTE ============
@app.route('/')
def index():
    return render_template('hero.html')

# ============ STUDENT DASHBOARD ROUTE ============
@app.route('/student')
def student_dash():
    return render_template('student-dashboard.html')


# ============ TEACHER DASHBOARD ROUTE ============
@app.route('/teacher')
def teacher_dash():
    return render_template('teacher-dashboard.html')


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='jimbo',
            email="jim@jim.com",
            password='password',
            course="test",
            role="Instructor"
        )
        models.User.create_user(
            username='joe student',
            email="joe@student.com",
            password='password',
            course="test",
            role="Student"
        )
        models.User.create_user(
            username='walrus',
            email="thewalrus@tusk.com",
            password='password',
            course="test",
            role="Instructor"
        )
    except ValueError:
        pass

app.run(debug=DEBUG, port=PORT)

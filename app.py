# ----------------------------------------------------------------------------------------
# Authors: Jonathan Jolivette | Matt Freeland | Enrique Morales
# Template Name: TA | Teacher's Assistant
# File: TA | APP.PY (MAIN FILE)
# App Version: 1.0
# ----------------------------------------------------------------------------------------

# from flask import render_template
from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from config import Config
import secrets
import os

import moment

import models
from models import User
from models import Event
import forms

# set debug and port defaults
DEBUG = True
PORT = 8000

# can bootstrap wrap the app and in turn cover the entire app where all
# templates are under the influence of bootstrap with the need for
# any cdn or linking to downloaded files/folders????
# Bootstrap(app)

app = Flask(__name__)
app.config.from_object(Config)

# initializing the login manager module
login_manager = LoginManager()
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
        if "generalassemb.ly" in form.email.data:
            flash("Registered as an instructor", 'success')
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                role="Instructor",
                password=form.password.data,
                course=form.course.data
            )
        else:
            flash("Registered as a student", 'success')
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                role="Student",
                password=form.password.data,
                course=form.course.data
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

# ============ EVENT PAGE ROUTE ============


@app.route('/event/',  methods=('GET', 'POST'))
@app.route('/event',  methods=('GET', 'POST'))
@login_required
def event():
    events = Event.select().order_by(Event.date, Event.time)
    return render_template('event.html', events=events)


# ============ EVENT CRUD ROUTES ============

# CREATE
@app.route('/event/create', methods=('GET', 'POST'))
@login_required
def create_event():
    form = forms.CreateEventForm()
    if g.user.role != "Instructor":
        flash("You must be an instructor to create events")
        return redirect(url_for('index'))

    if form.validate_on_submit():
        locator = Event.select().where(
            (Event.instructor == current_user.id) &
            (Event.date == form.date.data) &
            (Event.time == form.time.data))
        if locator.count() == 0:
            flash("Created New Event","success")
            models.Event.create_event(
                instructor=g.user.id,
                date=form.date.data,
                time=form.time.data,
            )
            return redirect(url_for("event"))
        else:
            flash("Event already exists","error")
            return redirect(url_for("event"))

    return render_template('create_event.html', form=form)

# DELETE
@app.route('/event/delete/<id>', methods=['DELETE', 'GET'])
@login_required
def event_delete(id):
    found_event = models.Event.get(models.Event.id == id)
    if g.user.id == found_event.instructor_id:
        if found_event.student != None:
            unlock_student = User.update(event_assigned = False).where(User.id == found_event.student)
            unlock_student.execute()
        event_to_delete = Event.delete().where(Event.id == found_event.id)
        event_to_delete.execute()
        flash("Deleted event successfully","error")
    else:
        flash("You don't have permission to delete this event.","error")
    return redirect(url_for('event'))

# UPDATE
@app.route('/event/update/<id>', methods=('POST', 'GET'))
def event_update(id):
    form = forms.EditEventForm()
    found_event = Event.get(Event.id == id)
    if g.user.id == found_event.instructor_id:
        if form.validate_on_submit():
            if found_event.date != form.date.data and found_event.time != form.time.data:
                locator = Event.select().where(
                    (Event.instructor == current_user.id) &
                    (Event.date == form.date.data) &
                    (Event.time == form.time.data))
                if locator.count() == 0:
                    update = Event.update(date=form.date.data, time=form.time.data).where(Event.id == id)
                    update.execute()
                    flash("Updated Event Successfully","success")
                    return redirect(url_for('event'))
            else:
                flash("Could not update, duplicate event exists","error")
                return redirect(url_for('event'))

    else:
        flash("You do not have permission to edit this event", "error")
        return redirect(url_for('event'))
    return render_template('edit_event.html', form=form, found_event=found_event)

# ADD STUDENT TO EVENT
@app.route('/event/add_student/<id>', methods=('POST', 'GET'))
def add_student_to_event(id):
    found_event = Event.get(Event.id == id)
    if found_event.student == None:
        add_student = Event.update(student=current_user.id).where(Event.id == id)
        add_student.execute()
        lock_events = User.update(event_assigned=True).where(User.id == current_user.id)
        lock_events.execute()
        flash("Checked in for event", "success")
        return redirect(url_for('event'))
    else:
        flash("Even already has a student assigned", "error")
    return redirect(url_for('event'))

# REMOVE STUDENT FROM EVENT
@app.route('/event/remove_student/<id>', methods=('POST', 'GET'))
def remove_student_from_event(id):
    found_event = Event.get(Event.id == id)
    if found_event.student == current_user:
        remove_student = Event.update(student_id=None).where(Event.id == id)
        remove_student.execute()
        unlock_events = User.update(event_assigned=False).where(User.id == current_user.id)
        unlock_events.execute()
        flash("Unscheduled successfully", "success")
    else:
        flash("Cannot unschedule other user events", "error")
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

# ============ Account update ROUTES ============

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # function returns filename without ext and ext itself,,,, underscores are a python way to throw away variables or "ignore"
    _, f_ext = os.path.splitext(form_picture.filename)
    # ignore photo name and concat hex with extension
    picture_fn = random_hex + f_ext
    # full path where image will be saved. full path of project directory
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

     # sets image resize with pillow
    output_size = (500, 500)
    # open image we passed into the function
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #saves at picture_path on file system
    i.save(picture_path)
    # return value to user
    return picture_fn


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = forms.UpdateAccountForm()
    if form.validate_on_submit():
        # if form.picture.data:
            # allows us to set users current image to profile picture
        picture_file = save_picture(form.picture.data)
        print(picture_file)
        update_image = User.update(image_file=picture_file).where(User.id == current_user.id)
        update_image.execute()
        # current_user.username = form.username.data
        # current_user.email = form.email.data
        # g.db.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_location = User.get(User.id == current_user.id)
    # decoded_location = image_location.image_file.decode()
    print(image_location.image_file)
    image_file = url_for('static', filename='profile_pics/' + image_location.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='jimbo',
            email="jim@jim.com",
            password='password',
            course="General",
            role="Instructor"
        )
        models.User.create_user(
            username='joe student',
            email="joe@student.com",
            password='password',
            course="General",
            role="Student"
        )
        models.User.create_user(
            username='walrus',
            email="thewalrus@tusk.com",
            password='password',
            course="General",
            role="Instructor"
        )
        models.User.create_user(
            username='rando calrissian',
            email="rando@student.com",
            password='password',
            course="General",
            role="Student"
        )
    except ValueError:
        pass

app.run(debug=DEBUG, port=PORT)

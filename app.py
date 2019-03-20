from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome

# from flask import render_template
app = Flask(__name__)
Bootstrap(app)

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
    app.secret_key = 'radish'
    app.run(debug=True, port=8000)

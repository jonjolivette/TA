from flask import Flask

# from flask import render_template

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'radish'

@app.route('/')
def index():
    return("Project3 - Ready to Rock")

@app.route('/dashboard')
def dashboard():
    return("Dashboard here")

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
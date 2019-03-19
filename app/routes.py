from app import app

@app.route('/')
def index():
    return("Project3 - Ready to Rock")

@app.route('/dashboard')
def dashboard():
    return("Dashboard here")
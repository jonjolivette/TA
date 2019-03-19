from flask import Flask

# from flask import render_template

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'radish'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
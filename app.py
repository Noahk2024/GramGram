from flask import Flask
from flask import render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

import os

db = SQLAlchemy()
app = Flask(__name__)
#bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('signin'))

    # show the form, it wasn't submitted
    return render_template('home.html')
    
#https://gramgram.ondigitalocean.app/health

@app.route('/health')
def health_check():
    return 'OK', 200

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/home/games")
def games():
    return render_template('games.html')
@app.route("/home/games/bingo")

def bingo():
    return render_template("bingo.html")
@app.route("/home/chat")
def chat():
    return render_template('base.html')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('base.html', name=name)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/login")
def login():
    return render_template("login.html")

app.debug = True
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    ###
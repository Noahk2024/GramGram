from flask import Flask, flash
from flask import render_template, request, url_for, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, EqualTo
from flask_bcrypt import Bcrypt
import os
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'hiddenkey'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    aboutme = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(80), nullable= False)
    

with app.app_context():
    db.create_all()


@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    if request.method == "POST":
        user_id = session["id"]
        friend_id = request.form['friend_id']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Check if the friendship already exists
        c.execute("SELECT * FROM Friends WHERE user_id = ? AND friend_id = ?", (user_id, friend_id))
        result = c.fetchone()
        if result is not None:
            error_msg = "You are already friends with this user."
            return render_template('addfriend.html', error=error_msg)

        # Add the friendship
        c.execute("INSERT INTO Friends (user_id, friend_id) VALUES (?, ?)", (user_id, friend_id))
        conn.commit()

        success_msg = "Friend added successfully."
        return render_template('addfriend.html', success=success_msg)
    return render_template("addfriend.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/dashboard/user_info")
def user_info():
    if 'username' not in session:
        return redirect(url_for('login'))

    #username = session['username']

    #conn = sqlite3.connect('database.db')
    #c = conn.cursor()

    # Retrieve the user's information
    #c.execute("SELECT * FROM Users WHERE username=?", (username,))
    #user = c.fetchone()

    # Close the database connection
    #conn.close()

    return render_template('userinfo.html', user=current_user)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/dashboard/chat')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# ...

@app.route('/dashboard/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('signup'))

    # show the form, it wasn't submitted
    return render_template('home.html')
    

@app.route('/health')
def health_check():
    return 'OK', 200

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/dashboard/games")
def games():
    return render_template('games.html')

@app.route("/dashboard/games/bingo")
def bingo():
    response = make_response(render_template("bingo.html"))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


#@app.route("/dashboard/chat")
#@login_required
#def chat():
#    return render_template('messagingservice.html', name=current_user.username)

@app.route('/dashboard')

def dashboard():
    username = session['username']

    # Get the friend IDs associated with the user's ID
   # conn = sqlite3.connect('database.db')
   # c = conn.cursor()

    # Retrieve the user's information
   # c.execute("SELECT * FROM Users WHERE username=?", (username,))
   # user = c.fetchone()
   # conn.close()
    return render_template('dashboard.html', user=current_user)

class SignupForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    aboutme = TextAreaField('About Me', validators=[DataRequired()])

    fullname = StringField('Full Name', validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired()])
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
    

#SIGN IN 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global current_user
    form = SignupForm()
    if request.method == 'POST':
        # process form data and save to database
        try:
            user = Users(username = form.username.data, password = form.password.data, fullname = form.fullname.data, aboutme = form.aboutme.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
            current_user = user
            session['username'] = user.username # store username in Flask session
            return redirect(url_for('home'))
        
        except Exception as e:
            db.session.rollback() # rollback the transaction if there is an error
            flash('An error occurred while creating your account. Please try again.', 'error')
            print(str(e))
    else:
        flash('An error occured while creating your account. Please try again.')
    return render_template('signup.html', form=form)
        # process form data


#LOGIN

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        # check if username and password are valid
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or user.password != form.password.data:
            form.username.errors.append('Invalid username or password')
            return render_template('login.html', form=form)
        session['username'] = user.username # store username in Flask session
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Query the database for the user ID with the given username
        c.execute("SELECT id FROM Users WHERE username = ?", (form.username.data,))
        result = c.fetchone()

        conn.close()
        session["id"] = result
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', form=form)

def get_user_details(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Retrieve the user's details from the database
    c.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    user_data = c.fetchone()

    # Close the database connection
    conn.close()

    # Return the user's details as a dictionary
    if user_data:
        user_details = {
            'id': user_data[0],
            'username': user_data[1],
            'password': user_data[3]
        }
        return user_details
    else:
        return None

@app.route("/dashboard/friends")

def friends():
    # Get the user ID based on their username from the session
    
    user_id = session["id"]
    username = session['username']

    # Get the friend IDs associated with the user's ID
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Retrieve the user's information
    c.execute("SELECT * FROM Users WHERE username=?", (username,))
    user = c.fetchone()

    c.execute("SELECT friend_id FROM Friends WHERE user_id = ?", (user_id,))
    friend_ids = [f[0] for f in c.fetchall()]
    conn.close()
    
    # Get the details of each friend and store them in a list of dictionaries
    friends_list = []
    for friend_id in friend_ids:
        friend_details = get_user_details(friend_id)
        friends_list.append(friend_details)

    # Render the template with the list of friends
    return render_template('friends.html', friends=friends_list, user=user)


@app.route("/home/aboutus")
def aboutus():
    return render_template('aboutus.html')

app.debug = True
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
from flask import Flask, flash
from flask import render_template, request, url_for, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/data')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# ...

@app.route('/create/', methods=('GET', 'POST'))
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
    #fullname = db.Column(db.String(90), nullable = True)

with app.app_context():
    db.create_all()

class SignInForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            print("username already exists")
            raise ValidationError(            
                'That username already exists. Please choose a different one.')
                


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

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


@app.route("/dashboard/chat")
@login_required
def chat():
    return render_template('messagingservice.html', name=current_user.username)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('base.html', name=current_user.username)

#SIGN IN 
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignInForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

#LOGIN
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard', name=user))
    return render_template('login.html', form=form)
#out
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/dashboard/friends")
@login_required
def friends():
    return render_template('friends.html')

@app.route("/display/user_info", methods=['GET', 'POST'])
@login_required
def user_info():
    if request.method == 'POST':
        #teste = request.form['full_name']
        
        #image = request.files['image'].read()

        userinfo = User(
            #test = "test"
            #user_id=current_user.id,
            #full_name=full_name,
            #bio=bio,
            #gender=gender,
            #age=age,
            #image=image
        )

        db.session.add(userinfo)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_userinfo.html') 

@app.route("/home/aboutus")
def aboutus():
    return render_template('aboutus.html')

app.debug = True
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
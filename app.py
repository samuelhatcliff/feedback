from flask import Flask, request, render_template, flash, redirect, render_template, jsonify
import psycopg2
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, User
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm

bcrypt = Bcrypt()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "topsecret1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/secrets')
def show_secrets():
    if "user_id" not in session:
        return redirect('/')
    return render_template('secrets.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user - User.register(username, password, email, first_name, last_name)
        
        session['user_id'] = new_user.username
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/secrets')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.username

            return redirect('/secrets')
        else:
            form.username.errors=["Invalid username or password. Please try again."]
    
    return render_template('login.html')

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')
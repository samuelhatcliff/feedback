from flask import Flask, request, render_template, flash, redirect, render_template, jsonify, session
import psycopg2
from flask_debugtoolbar import DebugToolbarExtension 
from models import connect_db, db, User, Feedback
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, AddFeedback, UpdateFeedback

bcrypt = Bcrypt()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "topsecret1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/users/<username_id>')
def show_user(username_id):
    if "user_id" not in session or int(username_id) != session['user_id']:
        return redirect('/')
    user = User.query.get(username_id)
    return render_template('user_profile.html', user = user)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return redirect(f'/users/{new_user.id}')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    print(LoginForm())
    print("^^^ OBER HEREEEE")
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.id

            return redirect(f'/users/{user.id}')
        else:
            form.username.errors=["Invalid username or password. Please try again."]
    
    return render_template('login.html', form=form)

@app.route('/users/<username_id>/delete', methods = ["POST"])
def delete_user(username_id):
    if "user_id" not in session or int(username_id) != session['user_id']:
        return redirect('/')
    user = User.query.get(username_id)
    db.session.delete(user)
    session.pop('user_id')
    db.session.commit()
    return redirect('/')

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')

@app.route('/users/<username_id>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username_id):
    if "user_id" not in session or int(username_id) != session['user_id']:
        return redirect('/')
    form = AddFeedback()
    user = User.query.get(username_id)
    if form.validate_on_submit():
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username = user.id
        )
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username_id}')
        
    
   
    return render_template('add_feedback.html', user=user, form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    form = UpdateFeedback()
    feedback = Feedback.query.get(feedback_id)
    user = User.query.get(feedback.username)
    if "user_id" not in session or int(user.id) != session['user_id']:
        return redirect('/')
    if form.validate_on_submit():
        feedback.content= form.content.data
        feedback.title= form.title.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')


    return render_template('update_feedback.html', feedback=feedback, form=form)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    user = User.query.get(feedback.username)
    if "user_id" not in session or int(user.id) != session['user_id']:
        return redirect('/')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{user.id}')


    
    
    
    
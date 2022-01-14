from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class RegisterForm(FlaskForm):
    '''form to add a new user. Username, password, and email required'''
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email")  
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    
    

class LoginForm(FlaskForm):
    '''form to login user with username and password'''
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
class AddFeedback(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])
    
class UpdateFeedback(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])

    
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import InputRequired, Optional, NumberRange, Email, email_validator

class RegisterForm(FlaskForm):
    """Form to register user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form to register user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form to submit feedback"""
    title = StringField("Post Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    username = HiddenField("Username")

class LogoutForm(FlaskForm):
    """Log user out"""

class DeleteForm(FlaskForm):
    """Delete user"""

class EditForm(FlaskForm):
    """Delete user"""
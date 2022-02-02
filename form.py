from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, Length, EqualTo

class SignUpForm(FlaskForm):
    username  = StringField(label='Username', validators=[DataRequired(),Length(min=6,max=50)])
    password  = PasswordField(label='Password', validators=[DataRequired(),Length(min=8,max=50)])
    cfpassword = PasswordField(label='Confirm Password', validators=[DataRequired(),EqualTo('password')])
    isadmin  = BooleanField(label='Is Admin', default=True)
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    loginusername  = StringField(label='Username', validators=[DataRequired(),Length(min=3,max=50)])
    loginpassword  = PasswordField(label='Password', validators=[DataRequired(),Length(min=3,max=50)])
    loginsubmit = SubmitField('Login')
from flask_wtf import Form
from wtforms import TextField
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, validators

class AdminSignUpForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    first_name = StringField('First Name', [validators.Length(min=6, max=35)])
    last_name = StringField('Last Name', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    admin_type = StringField('Administrator Type', [validators.Length(min=6, max=35)])
    submit = SubmitField('Submit')

class AdminLoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    submit = SubmitField('submit')

from flask_wtf import Form
from wtforms import TextField
from wtforms import Form, BooleanField, StringField, PasswordField, RadioField, DateField, IntegerField, SubmitField, validators, FileField

class AdminSignUpForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    first_name = StringField('First Name', [validators.Length(min=6, max=35)])
    last_name = StringField('Last Name', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    #admin_type = StringField('Administrator Type', [validators.Length(min=6, max=35)])

    submit = SubmitField('Submit')

class AdminLoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    submit = SubmitField('Submit')

class ReportDiseaseForm(Form):
    name = StringField('Name of Disease' , [validators.DataRequired()])
    date = DateField('Date of Report')
    age = IntegerField('Age of patient')
    gender = RadioField('Gender' , choices = [('male', 'Male') , ('female', 'Female')])
    file = FileField('Upload Report File')
    submit = SubmitField('Submit')
    
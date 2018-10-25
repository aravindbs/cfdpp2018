from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, current_user, logout_user, login_manager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo,config
from app.login import User
from app.forms.admin import AdminLoginForm, AdminSignUpForm, ReportDiseaseForm, ReportDeathForm
from datetime import datetime 
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return redirect(url_for('admin.login'))


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form.to_dict()
        user = mongo.db.users.find_one(
            {'email': login_data['email'], 'role': 'hcp'})
        if user:
            if check_password_hash(user['password'], login_data['password']):
                user_obj = User(user)
                login_user(user_obj)
                flash('Login Successful')
                return redirect(url_for('admin.dashboard', user=user['username']))
            else:
                flash("Incorrect Password")
                return redirect(url_for('admin.login'))
        else:
            flash("Unauthorized access")
            return redirect(url_for('admin.login'))
    form = AdminLoginForm()
    return render_template('admin/login.html', title=' Admin Login', form=form)


@admin.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form.to_dict()

        pwd = form_data['password']
        hashed_pwd = generate_password_hash(pwd)

        form_data['password'] = hashed_pwd
        if mongo.db.users.find_one({'email': form_data['email']}) or mongo.db.users.find_one({'username': form_data['username']}):
            user = mongo.db.users.find_one({'email': form_data['email']})
            if user and user['role'] == 'hcp':
                flash("Username Exists, Try Again")
                return redirect(url_for('admin.signup'))

        form_data['role'] = 'hcp'
        form_data.pop('confirm')
        mongo.db.users.update(
            {'username': form_data['username'], 'role': 'hcp'}, form_data, upsert=True)
        new_user = mongo.db.users.find_one(form_data)
        user = User(new_user)
        login_user(user)
        return redirect(url_for('admin.dashboard', user=current_user.username))

    args = request.args
    form = AdminSignUpForm()
 #   form_data = {}
    title = 'DiseaseWatch | Sign Up'
    if args:
        title = 'Moody | Edit Profile'
        user = args.get('user')
        form_data = mongo.db.users.find_one({'username': user})
        form_data.pop('password')
       
    return render_template('admin/signup.html',
                           title=title,
                           form=form,
                           )


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('admin.login'))


@admin.route('<user>/dashboard/')
@login_required
def dashboard(user):

    query = {'username': user, 'role': 'hcp'}
    user = mongo.db.users.find_one(query)
    return render_template('admin/dashboard.html', title='Admin', user=user)


@admin.route('<user>/reportdisease', methods=['GET', 'POST'])
@login_required
def reportdisease(user):
    form = ReportDiseaseForm()

    if request.method == 'POST':
        form_data = request.form.to_dict()
      
        for f in request.files.getlist('file'):
           
            if f.filename:
                filename = secure_filename(f.filename)
                f.save(os.path.join("app/static/files/", filename))
                url = "../static/files/" + filename 
        
                form_data['url'] = url 
                
        form_data.pop('submit')

        form_data['date'] = datetime.strptime(form_data['date'], "%Y-%m-%d")

        mongo.db.reports.insert(form_data)
        
    return render_template('admin/reportdisease.html', title = 'Report Disease', form = form)


@admin.route('<user>/reportdeath', methods=['GET', 'POST'])
@login_required
def reportdeath(user):
    form = ReportDeathForm()

    if request.method == 'POST':
        form_data = request.form.to_dict()
      
        for f in request.files.getlist('file'):
           
            if f.filename:
                filename = secure_filename(f.filename)
                f.save(os.path.join("app/static/files/", filename))
                url = "../static/files/" + filename 
        
                form_data['url'] = url 
                
        form_data.pop('submit')

        form_data['date'] = datetime.strptime(form_data['date'], "%Y-%m-%d")

        mongo.db.deaths.insert(form_data)

    return render_template('admin/reportdisease.html', title = 'Report Death', form = form)



    

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, current_user, logout_user, login_manager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo,config
from app.login import User
from app.forms.users import UserLoginForm, UserSignUpForm
import yaml, requests, json

from app.utils import get_plot_locations, get_current_location, get_dest_list

def load_config ():
    with open ('../config.yml') as f:
        config = yaml.load(f)
        return config 

config = load_config()
api = config['BING_API_KEY']

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form.to_dict()

        user = mongo.db.users.find_one(
            {'email': login_data['email'], 'role': 'user'})

        if user:
            if check_password_hash(user['password'], login_data['password']):
                user_obj = User(user)
                login_user(user_obj)
                flash('Login Successful')
                return redirect(url_for('users.dashboard', user=user['username']))
            else:
                flash("Incorrect Password")
                return redirect(url_for('users.login'))
        else:
            flash("Unauthorized Access")
            return redirect(url_for('users.login'))
    form = UserLoginForm()
    return render_template('users/login.html', title='Login', form=form)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form.to_dict()

        pwd = form_data['password']
        hashed_pwd = generate_password_hash(pwd)

        form_data['password'] = hashed_pwd
        if mongo.db.users.find_one({'email': form_data['email']}) or mongo.db.users.find_one({'username': form_data['username']}):
            user = mongo.db.users.find_one({'email': form_data['email']})
            if user and user['role'] == 'user':
                flash("Username Exists, Try Again")

                return redirect(url_for('users.signup'))
        form_data['role'] = 'user'
        form_data.pop('confirm')
        mongo.db.users.update(
            {'username': form_data['username'], 'role': 'user'}, form_data, upsert=True)
        new_user = mongo.db.users.find_one(form_data)
        user = User(new_user)
        login_user(user)
        return redirect(url_for('users.dashboard', user=current_user.username))

    args = request.args
    form = UserSignUpForm()
 
    title = 'DiseaseWatch | Sign Up'
    if args:
        title = 'DiseaseWatch | Edit Profile'
        user = args.get('user')
        form_data = mongo.db.users.find_one({'username': user})
        form_data.pop('password')
        
    return render_template('users/signup.html',  
                            title = title, 
                            form = form,
                            )


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('users.login'))


@users.route('/dashboard/<user>', methods=['GET', 'POST'])
@login_required
def dashboard(user):
    query = {'username': user, 'role': 'user'}
    user = mongo.db.users.find_one(query)

    if request.method == "POST":
        position = request.json

        query = {'username': current_user.username}
        position['username'] = current_user.username

        if mongo.db.current_loc.find_one({'username': current_user.username}):
            mongo.db.current_loc.update(query,  position, upsert=True)
        else:
            mongo.db.current_loc.insert(position)
        
            
    return render_template ('users/dashboard.html', title = 'Home | {username}'.format(username=current_user.username), user=user)

    return render_template('users/dashboard.html', title='Home | {username}'.format(username=user), user=user)


@users.route('/nearme/<user>', methods=['GET', 'POST'])
@login_required
def nearme(user):

    current_location = get_current_location(current_user.username)
    dest_list, disease_count, all_locs = get_dest_list()

    print(all_locs)
    data = {}
    origin_list = []
    origin_list.append(current_location)
    
    data["origins"] = origin_list
    data["destinations"] = dest_list
    data["travelMode"] = "driving"
   
    plot_locations = get_plot_locations(data, all_locs)

    return render_template('users/bing_map.html', api=api, current_location=current_location, plot_locations=plot_locations, disease_count=disease_count)
    
@users.route('/cityview/<user>',methods=['GET', 'POST'])
@login_required
def cityview(user):

    dest_list, disease_count, all_locs = get_dest_list()

    if request.method == "POST":
        form_data = request.form.to_dict()
        form_data["latitude"] = form_data.pop('lat')
        form_data["longitude"] = form_data.pop('lng')
        current_location = form_data
        
        data = {}
        origin_list = []
        origin_list.append(form_data)
        
        data["origins"] = origin_list
        data["destinations"] = dest_list
        data["travelMode"] = "driving"

        plot_locations = get_plot_locations(data, dest_list)
       
    return render_template('users/bing_map.html', api=api, current_location=current_location, plot_locations=plot_locations, disease_count=disease_count)


@users.route('/globalmap/<user>',methods=['GET', 'POST'])
@login_required
def globalmap(user):

    current_location = get_current_location(current_user.username)
    dest_list, disease_count, all_locs = get_dest_list()
    
    return render_template('users/bing_map.html', api=api, current_location=current_location, plot_locations=dest_list, disease_count=disease_count)
    



from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required,current_user, logout_user,login_manager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
from app.login import User
from app.forms.users import UserLoginForm, UserSignUpForm



users = Blueprint('users', __name__)

@users.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form.to_dict()
        print(login_data)
        user = mongo.db.users.find_one({'email': login_data['email'], 'role' : 'user'})
        print(user)
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
    return render_template('users/login.html', title='Login', form = form)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        pwd = form_data['password']
        hashed_pwd = generate_password_hash(pwd)
    
        form_data['password'] = hashed_pwd
        if mongo.db.users.find_one({ 'email' : form_data['email']}) or mongo.db.users.find_one({ 'username' : form_data['username']}):
            user = mongo.db.users.find_one({'email': form_data['email']})
            if user and user['role'] == 'user':
                flash("Username Exists, Try Again")
                print('here lol')
                return redirect(url_for('users.signup'))
        form_data['role'] = 'user'
        form_data.pop('confirm')
        mongo.db.users.update(
            {'username': form_data['username'], 'role' : 'user'}, form_data, upsert=True)
        new_user = mongo.db.users.find_one( form_data )
        user = User(new_user)
        login_user(user)
        return redirect(url_for('users.dashboard', user=current_user.username))  

    args = request.args
    form = UserSignUpForm()
 #   form_data = {}
    title = 'CFDPP | Sign Up'
    if args:
        title = 'Moody | Edit Profile'
        user = args.get('user')
        form_data = mongo.db.users.find_one({'username' : user})    
        form_data.pop('password')
        print (form_data)
    return render_template('users/signup.html',  
                            title = title, 
                            form = form,
                         #   form_data = form_data
                            )


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('users.login'))



@users.route('/dashboard/<user>',methods=['GET', 'POST'])
@login_required
def dashboard(user):
    query = {'username': user, 'role': 'user'}
    user = mongo.db.users.find_one(query)

    if request.method == "POST":
        position = request.json
        
        query = {'username' : current_user.username}
        position['username'] = current_user.username

        if mongo.db.current_loc.find_one({'username' : current_user.username}):
            mongo.db.current_loc.update(query, { '$set' : update } , upsert=True) 
        else: 
            mongo.db.current_loc.insert(position)
        
            
    return render_template ('users/dashboard.html', title = 'Home | {username}'.format(username=user), user=user)
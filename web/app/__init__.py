# main app init here

from flask import Flask, Blueprint

from flask_pymongo import PyMongo
from flask_login import LoginManager

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/testcfd'
app.secret_key = 'abcd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
mongo = PyMongo(app)

from app.views.admin import admin
from app.views.users import users
app.register_blueprint(users)
app.register_blueprint(admin, url_prefix='/admin')

from app.views import index
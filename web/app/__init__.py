# main app init here

from flask import Flask, Blueprint

from flask_pymongo import PyMongo
from flask_login import LoginManager
import yaml
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')  # initializes environment variables from the .env file 


app = Flask(__name__)


app.config['MONGO_URI'] = os.getenv('COSMOS_DB_URI')

app.secret_key = 'abcd'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
mongo = PyMongo(app)

from app.views.admin import admin
from app.views.users import users
app.register_blueprint(users)
app.register_blueprint(admin, url_prefix='/admin')

from app.views import index

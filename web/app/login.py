from app import login_manager, mongo
from flask_login import UserMixin, current_user
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user):
        self.id = str ( ObjectId(user['_id']))
        self.username = user['username']
        self.email = user['email']
        self.role = user['role']
        #self.logged_in = False


@login_manager.user_loader
def load_user(user_id):
   
    user = User(mongo.db.users.find_one({'_id': ObjectId(user_id)}))
    return user

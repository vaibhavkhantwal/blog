from api import db,login_manager
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)    

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,nullable=False ,primary_key=True)
    username = db.Column(db.String(64),nullable=False, unique=True)
    email = db.Column(db.String(120),nullable=False, unique=True)
    password = db.Column(db.String(256),nullable=False)
    posts=db.relationship('Post',backref='author')

class Post(db.Model):
    id=db.Column(db.Integer,nullable=False ,primary_key=True)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    story=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    pictures=db.relationship('Picture',backref='parent_post',cascade="all, delete-orphan")

class Picture(db.Model):
    id=db.Column(db.Integer,nullable=False,primary_key=True)
    link=db.Column(db.String(50),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


# Define the Bug model
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#define user model 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed passwords
    bugs = db.relationship('Bug', backref='user')
    

    

    
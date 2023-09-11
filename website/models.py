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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


#define user model 
class User(db.Model, UserMixin):
    """
    Represents a user in the application.

    Attributes:
        id (int): A unique identifier for the user.
        email (str): The email address associated with the user (unique and non-nullable).
        username (str): The username chosen by the user (non-nullable).
        password (str): The hashed password for the user (non-nullable).
        bugs (Relationship): A relationship to the 'Bug' model representing bugs associated with this user.

    Relationships:
        - 'bugs': This user's reported bugs. Allows access to bugs created by this user.

    Notes:
        - This class represents a user in the application's database.
        - It inherits from both 'db.Model' (indicating it's an SQLAlchemy model) and 'UserMixin'
          (providing default user-related methods for Flask-Login).
        - The 'id' field is an auto-incremented integer primary key.
        - 'email' is a unique string representing the user's email address (used for authentication).
        - 'username' is a non-unique string representing the user's chosen username.
        - 'password' stores the user's hashed password, ensuring security.
        - The 'bugs' relationship is used to access bugs created by this user.
        - Lazy loading is enabled for the 'bugs' relationship, meaning that bugs are loaded only when accessed.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed passwords
    bugs = db.relationship('Bug', backref='user', lazy=True)
    

    

    
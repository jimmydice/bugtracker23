from . import db
from flask_login import UserMixin  # required for managing user sessions and authentication.
from datetime import datetime


# Define the Bug model
class Bug(db.Model):
    """
    Represents a bug report in the application.

    Attributes:
        id (int): A unique identifier for the bug.
        title (str): The title or summary of the bug (non-nullable).
        description (str): A detailed description of the bug (non-nullable).
        status (str): The current status of the bug (non-nullable).
        priority (str): The priority level assigned to the bug (non-nullable).
        date_created (datetime): The date and time when the bug was created (non-nullable).
        user_id (int): The user identifier associated with the bug report (foreign key, non-nullable).

    Relationships:
        - 'user': The user who reported this bug.

    Notes:
        - This class represents a bug report in the application's database.
        - It inherits from 'db.Model', indicating it's an SQLAlchemy model.
        - The 'id' field is an auto-incremented integer primary key.
        - 'title' is a short, descriptive title or summary of the bug.
        - 'description' provides a more detailed description of the bug.
        - 'status' represents the current status of the bug (e.g., 'Open', 'In Progress', 'Resolved').
        - 'priority' indicates the priority level of the bug (e.g., 'Low', 'Medium', 'High').
        - 'date_created' records the date and time when the bug report was created.
        - 'user_id' is a foreign key linking the bug report to the user who reported it.
        - The 'user' relationship allows accessing the user associated with this bug.
    """
    id = db.Column(db.Integer, primary_key=True)  #primary_key: uniquely identifies each row of a table. 
    #It gets a unique index for each primary key column that helps with faster access
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # foreign key reference to the user who created the bug

    # nullable=False is used to define a constraint on a database column, indicating that the column must always have a value, 
    # and it cannot be left empty or null. In other words, it enforces that the column should not contain missing or undefined data.


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
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    bugs = db.relationship('Bug', backref='user', lazy=True)
    # Lazy loading means that the related objects are not loaded from the database until they are explicitly accessed or requested by your code
     


    

    
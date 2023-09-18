#  Initializes the Flask application, configures the database, and registers blueprints for different parts of the app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager  #handles user authentication



# Configure the SQLite database path
db = SQLAlchemy()  # creates an instance of SQLAlchemy
DB_NAME = "database.db"  # Specifies the name of the SQLite database file to be used


def create_app():
    """
    Create and configure the Flask application.

    This function initializes and configures a Flask web application. It sets up the application's configuration,
    database connection, blueprints, and user authentication.

    Returns:
        Flask: The configured Flask application.

    Notes:
        - The application's configuration includes the secret key and the database URI.
        - SQLAlchemy is initialized for the Flask app, enabling database operations.
        - Blueprints for different parts of the application (views and authentication) are registered.
        - User authentication using Flask-Login is configured, specifying the login view and user loader.
        - The database tables are created if they do not already exist.
    """
    app = Flask(__name__, static_folder='static')
    # Configure the secret key and database URI
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'   #if you want to use environmenal variables then: os.environ.get('ENV', f'sqlite:///{DB_NAME}')
    
    # Initialize the SQLAlchemy extension for the Flask app.
    db.init_app(app)  

    # Import views and authentication blueprints
    from .views import views 
    from .auth import auth

    #register the blueprint with our flask app
    app.register_blueprint(views, url_prefix='/')  
    app.register_blueprint(auth, url_prefix='/')

    
    # ensure that my models are available when needed for database operations and follows best practices for structuring Flask applications.
    from .models import User, Bug  

    # Configure user authentication using Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  #where do we need to go if we are not logged in. It redirects us in auth.login. 
    login_manager.init_app(app)  #we are telling login_manager which app we are using. 

    #this is telling flask how we load a user. 
    @login_manager.user_loader  
    def load_user(id):
        """
        Load a user from the database.

        Args:
            id (int): The user's ID.

        Returns:
            User: The user object associated with the provided ID.
        """
        return User.query.get(int(id))  
    
    # Create database tables based on the models i have defined if they do not exist. 
    with app.app_context():  # context is a context manager that provides access to various application-specific resources, 
        # including the application configuration and extensions like the database. 
        # # The app.app_context() call creates a context within which you can work with these resources.
        db.create_all()
    
    

    return app


def create_database(app):
    """
    Create the SQLite database if it does not exist.

    Checks if the SQLite database file specified by 'DB_NAME' exists. If it does not exist,
    it creates the database and its tables based on the SQLAlchemy models.

    Args:
        app (Flask): The Flask application for which the database is created.

    Notes:
        - The 'DB_NAME' constant specifies the name of the SQLite database file.
        - The 'db.create_all(app=app)' statement creates the database tables based on the models defined in the app.
        - A message is printed to indicate that the database has been created.

    Returns:
        None
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)  #we pass app because we need to tell flask SQLalchemy for which app we are creating the database 
        print('Created User Database!')




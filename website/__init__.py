from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from datetime import datetime
from flask_login import LoginManager  # we need to tell our flask in general how we actually log in a user


# Configure the SQLite database path (replace 'path/to/database.db' with your actual path)
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{USERS}'
    db.init_app(app)

    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')  #register the blueprint with our flask app
    app.register_blueprint(auth, url_prefix='/')

    #i added those lines below when i tried to create the user  27 - 37
    from .models import User, Bug  #we import .models in our __init_.py because we have to make sure that we load this file and that 
    # this file runs (this models.py file) and defines these classes before we initialise or create our database. 

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  #where do we need to go if we are not logged in. It redirects us in auth.login. 
    login_manager.init_app(app)  #we are telling login_manager which app we are using. 

    @login_manager.user_loader  #this is telling flask how we load a user. 
    def load_user(id):
        return User.query.get(int(id))  # we dont need to define that id=id because by default it searched the id.  
        # we pass an id to the load_user(id) and then it returns the user with this id. 

    with app.app_context():
        db.create_all()
    #initialize_database()
    

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)  #we pass app because we need to tell flask SQLalchemy which app we are creating the database for 
        print('Created User Database!')




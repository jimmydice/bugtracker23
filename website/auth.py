from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user  
from .password import is_valid_password


auth = Blueprint('auth', __name__)  #Flask Blueprint named 'auth' that can be used to define routes, views, 
#and other functionality related to user authentication within my Flask application.


@auth.route('/account-settings', methods=['GET'])
@login_required
def account_settings():
    return render_template('account_settings.html', user=current_user)


@auth.route('/update-username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form.get('new_username')
    current_user.username = new_username
    db.session.commit()
    flash('Username updated successfully!', category='success')
    return redirect(url_for('auth.account_settings'))



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # searching if this user exists in our db by searching emails. 
        # It will return the first result 
        if user:
            if check_password_hash(user.password, password):  #it searches if the password the user enters matches the hash we have stored in our data center. 
                login_user(user, remember=True)  #remembers that the user is logged in while the server is running 
                return redirect(url_for('views.index'))  # redirect user to the home page after he logs in. 
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('User does not exist.', category='danger')
    
    # Check if the user is not authenticated
    #if not current_user.is_authenticated:
    #flash('Please log in to access this page.', category='info')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required  # makes sure we cannot access this page unless the user is logged in. 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='danger')  #making sure that a user cannot sign up again with the same email. 
        elif len(email) < 10:
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(username) < 3:
            flash('First name must be greater than 2 characters.', category='danger')
        elif not is_valid_password(password1):
            flash('Password must be at least 6 characters long and contain at least one special character.', category='danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='danger')
        
            

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='scrypt'))
            db.session.add(new_user)  # adds the new user to the database 
            db.session.commit()  #commit the changes. Updates the database with the new user. 

            login_user(new_user, remember=True)  #remembers that the user is logged in while the server is running 
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))  #after the user us created we redirect him to the homepage. 
            # To do this we have ti import for flask 'redirect' and 'url_for'. 
            # we use 'views.home' because if the route ever changes this -> (url_for('views.home') will pick it up. So if finds a URL associated
            # with this function 

    return render_template("sign_up.html") 
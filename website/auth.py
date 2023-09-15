from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db, Bug
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


@auth.route("/update-password", methods=['POST'])
@login_required
def update_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    new_password2 = request.form.get('new_password2')
    if not check_password_hash(current_user.password, old_password):
        flash('Current password is incorrect!', category='danger')
    elif not is_valid_password(new_password):
            flash('Password must be at least 6 characters long and contain at least one special character.', category='danger')
    elif new_password != new_password2:
        flash('Passwords don\'t match.', category='danger')

    else:
        current_user.password = generate_password_hash(new_password, method='scrypt')
        db.session.commit()
        flash('Password updated successfully!', category='success')
    
    return redirect(url_for('auth.account_settings'))


@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    # Render the confirmation page
    return render_template('confirm_delete.html')


@auth.route('/confirm-delete', methods=['POST'])
@login_required
def delete_account_2():
    """
    Handle the deletion of the user's account.

    This function deletes the user's account and associated data, such as bugs,
    when the user initiates an account deletion request.

    Returns:
        Flask Response: A redirect to the login page or another page after successful
        account deletion. In case of an error, it redirects back to the account settings
        page with an error message.

    Raises:
        Exception: If any unexpected error occurs during the account deletion process,
        it will be caught, and the user will be informed with an error message.
    """
    try:
        # Check if the user confirmed the deletion
        confirmation = request.form.get('confirm')
        # If the user didn't confirm, redirect back to account settings
        if confirmation == 'no':
            # If the user didn't confirm, redirect back to account settings
            flash('Account deletion was canceled.', category='warning')
            return redirect(url_for('auth.account_settings'))

        elif confirmation == 'yes':
            # Get the user's account and associated bugs
            user = current_user
            bugs = Bug.query.filter_by(user_id=user.id).all()

            # Delete associated bug related to this user
            for bug in bugs:
                db.session.delete(bug)

            # Delete the user's account
            db.session.delete(user)
            db.session.commit()

            # Logout the user after account deletion
            logout_user()
            print("Your account has been deleted successfully")
            flash('Your account has been deleted successfully.', category='success')
        
        return redirect(url_for('auth.login'))  # Redirect to the login page or another page

        # If the user didn't confirm, redirect back to account settings
        # flash('Account deletion was canceled.', category='info')
        # return redirect(url_for('auth.account_settings'))

    except Exception as e:
        flash(f'An error occurred: {str(e)}', category='danger')
        return redirect(url_for('auth.account_settings'))  # Redirect back to account settings on error



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
        elif len(email) < 10 and '@' not in email:
            flash('Please enter a valid email address.', category='danger')
        elif len(username) < 3:
            flash('First name must be greater than 2 characters.', category='danger')
        elif not is_valid_password(password1):
            flash('Password must be at least 6 characters long and contain at least one special character.', category='danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='danger')
        
            

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # adds the new user to the database 
            db.session.commit()  #commit the changes. Updates the database with the new user. 

            login_user(new_user, remember=True)  #remembers that the user is logged in while the server is running 
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))  #after the user us created we redirect him to the homepage. 
            # To do this we have ti import for flask 'redirect' and 'url_for'. 
            # we use 'views.home' because if the route ever changes this -> (url_for('views.home') will pick it up. So if finds a URL associated
            # with this function 

    return render_template("sign_up.html") 
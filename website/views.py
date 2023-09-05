from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user 
from . import db
import json
from .models import Bug, User
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def index():
    """Fetch bug data from the database and pass it to the template"""
    bugs = Bug.query.filter_by(user=current_user).all()
    return render_template('index.html', bugs=bugs, user=current_user)



@views.route('/json', methods=['GET'])
@login_required
def get_bugs():
    """get bugs in json format"""
    bugs = Bug.query.all()
    bug_list = []
    for bug in bugs:
        bug_dict = {
            'id': bug.id,
            'title': bug.title,
            'description': bug.description,
            'status': bug.status,
            'priority': bug.priority,
            'date_created': bug.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }
        bug_list.append(bug_dict)
    return jsonify(bug_list)


@views.route('/bugs', methods=['POST'])
@login_required
def create_bug():
    """Creates a bug and updates the bug database"""
    data = request.json
    bug = Bug(
        title=data['title'], 
        description=data['description'], 
        status=data['status'], 
        priority=data['priority'],
        date_created=datetime.utcnow(),  # Set the current date and time
        user_id=current_user.id  # Set the user_id to the ID of the currently logged-in user
    )
    
    db.session.add(bug)
    db.session.commit()
    return jsonify({'message': 'Bug created successfully', 'bug_id': bug.id}), 201


@views.route('/bugs/<int:bug_id>', methods=['PUT'])
@login_required
def update_bug(bug_id):
    """Updates a bug"""
    bug = Bug.query.get_or_404(bug_id)
    data = request.json
    bug.title = data['title']
    bug.description = data['description']
    bug.status = data['status']
    bug.priority = data['priority']
    db.session.commit()
    return jsonify({'message': 'Bug updated successfully'}), 200


@views.route('/bugs/<int:bug_id>', methods=['DELETE'])
@login_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()
    return jsonify({'message': 'Bug deleted successfully'}), 200


@views.route('/search')
@login_required
def search_bug():
    keyword = request.args.get('keyword')
    category = request.args.get('category')

    # Query the database based on the provided keyword and category
    if category == 'title':
        bugs = Bug.query.filter(Bug.title.ilike(f'%{keyword}%')).all()
    elif category == 'status':
        bugs = Bug.query.filter(Bug.status.ilike(f'%{keyword}%')).all()
    elif category == 'priority':
        bugs = Bug.query.filter(Bug.priority.ilike(f'%{keyword}%')).all()
    elif category == 'date_created':
        # Convert the keyword to a datetime object and query the database
        try:
            keyword_date = datetime.strptime(keyword, '%Y-%m-%d %H:%M:%S')
            bugs = Bug.query.filter(Bug.date_created == keyword_date).all()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    else:
        return jsonify({'error': 'Invalid category'}), 400


    # Convert the bugs to a list of dictionaries for JSON response
    bug_list = []
    for bug in bugs:
        bug_dict = {
            'id': bug.id,
            'title': bug.title,
            'description': bug.description,
            'status': bug.status,
            'priority': bug.priority,
            'date_created': bug.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }
        bug_list.append(bug_dict)

    return jsonify(bug_list)


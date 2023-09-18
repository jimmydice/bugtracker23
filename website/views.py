from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user 
from . import db
import json
from .models import Bug, User
from datetime import datetime


views = Blueprint('views', __name__)
# The views blueprint contains routes for the homepage, bug creation, bug listing, bug updates, and bug searches.



# These routes handle HTTP requests and render HTML templates
@views.route('/')
@login_required
def index():
    """Fetch bug data from the database and pass it to the template"""
    bugs = Bug.query.filter_by(user=current_user).all()
    return render_template('index.html', bugs=bugs, user=current_user)



@views.route('/json', methods=['GET'])
@login_required
def get_bugs():
    """
    Retrieves a list of bug reports in JSON format.

    Returns:
        JSON: A JSON representation of bug reports with their attributes.

    Notes:
        - This function queries the database for all bug reports.
        - It constructs a list of dictionaries, where each dictionary represents a bug report.
        - The dictionaries contain the following bug attributes:
          - 'id': The unique identifier of the bug.
          - 'title': The title or summary of the bug.
          - 'description': A detailed description of the bug.
          - 'status': The current status of the bug.
          - 'priority': The priority level assigned to the bug.
          - 'date_created': The date and time when the bug report was created, formatted as 'YYYY-MM-DD HH:MM:SS'.
        - The list of bug dictionaries is then converted to JSON format using Flask's 'jsonify' function.
        - This endpoint is typically used to retrieve a list of bug reports in a machine-readable format, e.g., for
          consumption by a front-end application or for exporting bug data.

    Example:
        An example of the JSON response for two bug reports might look like this:
        [
            {
                'id': 1,
                'title': 'UI Alignment Issue',
                'description': 'The elements on the page are not aligned properly.',
                'status': 'Open',
                'priority': 'High',
                'date_created': '2023-09-09 14:30:00'
            },
            {
                'id': 2,
                'title': 'Authentication Bug',
                'description': 'Users are unable to log in.',
                'status': 'Resolved',
                'priority': 'Medium',
                'date_created': '2023-09-08 10:15:00'
            }
        ]
    """
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


@views.route('/bugs', methods=['POST'])  #It is triggered when the JavaScript function sends a POST request to the /bugs endpoint.
@login_required
def create_bug():
    """
    Create a new bug report and update the bug database.

    Args:
        None (data is provided in the request JSON).

    Returns:
        JSON: A JSON response indicating the success of the bug creation and the new bug's ID.

    Notes:
        - This function is used to create a new bug report based on the data provided in the request JSON.
        - The required attributes for creating a bug report include 'title', 'description', 'status', and 'priority'.
        - The 'date_created' attribute is automatically set to the current date and time using 'datetime.utcnow()'.
        - The 'user_id' attribute is set to the ID of the currently logged-in user using 'current_user.id'.
        - The newly created bug is added to the database session and committed to the database.
        - A JSON response is returned to confirm the successful creation of the bug report, along with the new bug's ID.
        - The response status code '201 Created' indicates a successful creation.

    Example Request (JSON):
        {
            'title': 'UI Alignment Issue',
            'description': 'The elements on the page are not aligned properly.',
            'status': 'Open',
            'priority': 'High'
        }

    Example Response (JSON):
        {
            'message': 'Bug created successfully',
            'bug_id': 1
        }
    """
    data = request.json  #  extracts the bug data from the JSON request using request.json.
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


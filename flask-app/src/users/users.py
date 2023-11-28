from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

users = Blueprint('users', __name__)

# Get user account for specific user
@users.route('/users/<username>', methods=['GET'])
def get_user_account(username):
    cursor = db.get_db().cursor()
    cursor.execute('select * from users where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Create user account for new user
@users.route('/users/', methods=['POST'])
def add_new_user():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['product_name']
    description = the_data['product_description']
    price = the_data['product_price']
    category = the_data['product_category']

    # Constructing the query
    query = 'insert into products (product_name, description, category, list_price) values ("'
    query += name + '", "'
    query += description + '", "'
    query += category + '", '
    query += str(price) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
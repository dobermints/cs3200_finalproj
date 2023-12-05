from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

users = Blueprint('users', __name__)

# Create user account for new user
@users.route('/users', methods=['POST'])
def add_new_user():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    username = the_data['username']
    first_name = the_data['first_name']
    last_name = the_data['last_name']
    country = the_data['country']
    date_joined = the_data['date_joined']
    phone = the_data['phone']
    email = the_data['email']
    date_of_birth = the_data['date_of_birth']
    
    # Constructing the query
    query = 'insert into User (username, firstName, lastName, country, dateJoined, phone, email, dateOfBirth) values ("'
    query += username + ', '
    query += first_name + ', '
    query += last_name + ', '
    query += country + ', '
    query += date_joined + ', '
    query += str(phone) + ', '
    query += email + ', '
    query += str(date_of_birth) + ');'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get user account for specific user
@users.route('/users/<username>', methods=['GET'])
def get_user_account(username):
    cursor = db.get_db().cursor()
    cursor.execute('select * from User where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update user account for specific user
@users.route('/users/<username>', methods=['PUT'])
def update_user_account(username):
    cursor = db.get_db().cursor()
    the_data = request.json
    current_app.logger.info(the_data)
    
    # grab username and previous unchangeable details
    userInfo = get_user_account(username)

    prevDateJoined = userInfo['dateJoined']
    prevCountry = userInfo['country']
    prevPhone = userInfo['phone']
    prevDOB = userInfo['dateOfBirth']
    prevEmail = userInfo['email']
    prevFirstName = userInfo['firstName']
    prevLastName = userInfo['lastName']
    prevUsername = userInfo['username']

    # changeable details
    email = the_data['email']
    firstName = the_data['firstName']
    lastName = the_data['lastName']
    country = the_data['country']
    phone = the_data['phone']
    dob = the_data['dateOfBirth']
    
    query = 'UPDATE User SET '
    query += 'email = ' + str(email) + ', '
    query += 'firstName = ' + str(firstName) + ', '
    query += 'lastName = ' + str(lastName) + ', '
    query += 'country = ' + str(country) + ', '
    query += 'phone = ' + str(phone) + ', '
    query += 'dateOfBirth = ' + str(dob) + ' '
    query += 'WHERE username = {0};'.format(username)

    cursor.execute(query)
    current_app.logger.info(query)
    
    db.get_db().commit()
    return 'Successful deletion'

# Delete user account for specific user
@users.route('/users/<username>', methods=['DELETE'])
def delete_user_account(username):
    cursor = db.get_db().cursor()
    
    query = 'delete from User where username = {0};'.format(username)
    cursor.execute(query)
    current_app.logger.info(query)
    
    db.get_db().commit()
    return 'Successful deletion'

# Gets a list of the friends of a user
@users.route('/users/friends/<username>', methods=['GET'])
def get_user_friends(username):
    cursor = db.get_db().cursor()
    cursor.execute('select * from User JOIN (select * Friends where requestUsername = {0}'.format(username) + ') as a ON a.acceptUsername = User.username;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a friendship between two users
@users.route('/users/friends/', methods=['POST'])
def add_friendship():
    cursor = db.get_db().cursor()
    the_data = request.json
    current_app.logger.info(the_data)
    
    usernameReq = the_data['requestUsername'] 
    usernameAcc = the_data['acceptUsername'] 
    
    query = 'INSERT INTO Friends (requestUsername, acceptUsername) VALUES (' + usernameReq + ' AND acceptUsername = {0});'.format(usernameAcc)
    cursor.execute(query)
    current_app.logger.info(query)
    db.get_db().commit()
    return 'Successful post'

# Remove a friendship between two users
@users.route('/users/friends/<usernameReq>/<usernameAcc>', methods=['DELETE'])
def delete_friendship(usernameReq, usernameAcc):
    cursor = db.get_db().cursor()
    query = 'DELETE * from Friends WHERE requestUsername = {0}'.format(usernameReq) + ' AND acceptUsername = {0};'.format(usernameAcc)
    cursor.execute(query)
    current_app.logger.info(query)
    db.get_db().commit()
    return 'Successful deletion'
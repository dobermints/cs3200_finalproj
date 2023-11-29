from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

artists = Blueprint('artists', __name__)

# Get user account for specific user
@artists.route('/artists/<username>', methods=['GET'])
def get_artist_account(username):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Artist where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get artist rank based off artist username
@artists.route('/artists/<rank>', methods=['GET'])
def get_artist_rank(username):
    cursor = db.get_db().cursor()
    cursor.execute('select dayRank, monthRank, weekRank from Artist where username = {0}'.format(username))
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
@artists.route('/artists/', methods=['POST'])
def add_new_artist():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    username = the_data['username']
    first_name = the_data['first_name']
    last_name = the_data['last_name']
    stage_name = the_data['stage_name']
    country = the_data['country']
    date_joined = the_data['date_joined']
    phone = the_data['phone']
    email = the_data['email']
    dayRank = the_data['dayRank']
    monthRank = the_data['monthRank']
    weekRank = the_data['weekRank']
    total_dislikes = the_data['total_dislikes']
    total_likes = the_data['total_likes']
    date_of_birth = the_data['date_of_birth']
    
    # Constructing the query
    query = 'insert into Artist (username, firstName, lastName, stageName, country, dateJoined, phone, email, dayRank, monthRank, weekRank, totalDislikes, totalLikes, dateOfBirth) values ("'
    query += username + '", "'
    query += first_name + '", "'
    query += last_name + '", '
    query += stage_name + '", "'
    query += country + '", "'
    query += date_joined + '", "'
    query += str(phone) + '", '
    query += email + '", '
    query += str(dayRank) + '", "'
    query += str(monthRank) + '", "'
    query += str(weekRank) + '", "'
    query += str(total_dislikes) + '", "'
    query += str(total_likes) + '", '
    query += str(date_of_birth) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Update user account for specific user
@artists.route('/artists/row/<row>', methods=['PUT'])
def update_artist_account(username):
    cursor = db.get_db().cursor()
    cursor.execute('update Artist set where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete user account for specific user
@artists.route('/artists/deleted', methods=['DELETE'])
def delete_artist_account(username):
    cursor = db.get_db().cursor()
    cursor.execute('delete from Artist where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
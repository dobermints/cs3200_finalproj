from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

artists = Blueprint('artists', __name__)

# Get user account for all artists
@artists.route('/artists', methods=['GET'])
def get_all_artist_account():
    cursor = db.get_db().cursor()
    cursor.execute('select * from Artist')
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
@artists.route('/artists', methods=['POST'])
def add_new_artist():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    username = the_data['username']
    first_name = the_data['firstName']
    last_name = the_data['lastName']
    stage_name = the_data['stageName']
    email = the_data['email']
    phone = the_data['phone']
    country = the_data['country']
    date_of_birth = the_data['dateOfBirth']
    genre = the_data['genre']
    
    # Constructing the query
    query = 'insert into Artist (username, firstName, lastName, stageName, country, phone, email, genre, dateOfBirth) values ('
    query += '"' + username + '", '
    query += '"' + first_name + '", '
    query += '"' + last_name + '", '
    query += '"' + stage_name + '", '
    query += '"' + country + '", '
    query += '"' + str(phone) + '", '
    query += '"' + email + '", '
    query += '"' + genre + '", '
    query += '"' + str(date_of_birth) + '");'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'





# Delete an artist profile based on username
@artists.route('/artists/<username>', methods=['DELETE'])
def delete_artist_account(username):
    cursor = db.get_db().cursor()
    
    query = 'delete from Artist where username = {0};'.format(username)
    cursor.execute(query)
    current_app.logger.info(query)
    
    db.get_db().commit()
    return 'Successful deletion'

# Get user account for specific user
@artists.route('/artists/<username>', methods=['GET'])
def get_an_artist_account(username):
    cursor = db.get_db().cursor()
    cursor.execute('select username, stageName, country, dateJoined, totalLikes, totalDislikes, dayRank, weekRank, monthRank from Artist where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update account for specific artist
@artists.route('/artists/<username>', methods=['PUT'])
def update_artist_account(username):
    cursor = db.get_db().cursor()
    the_data = request.json
    current_app.logger.info(the_data)
    
    # grab username and previous unchangeable details
    artistInfo = get_an_artist_account(username)

    prevGenre = artistInfo['genre']
    prevLanguage = artistInfo['language']
    prevTitle = artistInfo['title']
    prevEmail = artistInfo['email']
    prevStageName = artistInfo['stageName']
    prevCountry = artistInfo['country']
    prevPhone = artistInfo['phone']
    prevDOB = artistInfo['dateOfBirth']
    prevTotalLikes = artistInfo['totalLikes']
    prevTotalDislikes = artistInfo['totalDislikes']
    prevDayRank = artistInfo['dayRank']
    prevWeekRank = artistInfo['weekRank']
    prevMonthRank = artistInfo['monthRank']
    
    # changeable details
    genre = the_data['genre']
    stageName = the_data['stageName']
    email = the_data['email']
    firstName = the_data['firstName']
    lastName = the_data['lastName']
    country = the_data['country']
    phone = the_data['phone']
    dob = the_data['dateOfBirth']
    
    query = 'UPDATE Artist SET '
    query += '"' + 'genre = ' + str(genre) + '", '
    query += '"' + 'stageName = ' + str(stageName) + '", '
    query += '"' + 'email = ' + str(email) + '", '
    query += '"' + 'firstName = ' + str(firstName) + '", '
    query += '"' + 'lastName = ' + str(lastName) + '", '
    query += '"' + 'country = ' + str(country) + '", '
    query += '"' + 'phone = ' + str(phone) + '", '
    query += '"' + 'dateOfBirth = ' + str(dob) + '" '
    query += '"' + 'WHERE username = {0};'.format(username)

    cursor.execute(query)
    current_app.logger.info(query)
    
    db.get_db().commit()
    return 'Success!'

# Get artist rank based off artist username
@artists.route('/artists/rank/<stageName>', methods=['GET'])
def get_artist_rank(stageName):
    cursor = db.get_db().cursor()
    cursor.execute("select stagename, dayRank, monthRank, weekRank from Artist where stageName LIKE '%{0}%';".format(" ".join(stageName.split("+"))))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get artists based off artist genre
@artists.route('/artists/genre/<genre>', methods=['GET'])
def get_artist_by_genre(genre):
    cursor = db.get_db().cursor()
    cursor.execute('select username, stageName, country, dateJoined, totalLikes, totalDislikes, dayRank, weekRank, monthRank from Artist where genre = {0}'.format(genre))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get totalLikes of an artist
@artists.route('/artists/likes/<username>', methods=['GET'])
def get_artist_likes(username):
    cursor = db.get_db().cursor()
    cursor.execute('select totalLikes from Artist where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get totalDisikes of an artist
@artists.route('/artists/dislikes/<username>', methods=['GET'])
def get_artist_dislikes(username):
    cursor = db.get_db().cursor()
    cursor.execute('select totalDislikes from Artist where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

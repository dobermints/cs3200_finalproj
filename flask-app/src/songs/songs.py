from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

songs = Blueprint('songs', __name__)

# Get song based on songID
@songs.route('/songs/<songID>', methods=['GET'])
def get_song(songID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Song where songID = {0}'.format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get song rank based off songID
@songs.route('/songs/<rank>', methods=['GET'])
def get_song_rank(songID):
    cursor = db.get_db().cursor()
    cursor.execute('select dayRank, monthRank, weekRank from Song where songID = {0}'.format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add song to the app for an artist
@songs.route('/songs/', methods=['POST'])
def create_song():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    songID = the_data['songID']
    genre = the_data['genre']
    language = the_data['language']
    title = the_data['title']
    duration = the_data['duration']
    dateReleased = the_data['dateReleased']
    dayRank = the_data['dayRank']
    monthRank = the_data['monthRank']
    weekRank = the_data['weekRank']
    dislikes = the_data['dislikes']
    likes = the_data['likes']
    artistUsername = the_data['artistUsername']
    
    # Constructing the query
    query = 'insert into Song (songID, genre, language, title, duration, dateReleased, dayRank, monthRank, weekRank, dislikes, likes, artistUsername) values ("'
    query += str(songID) + '", "'
    query += genre + '", "'
    query += language + '", "'
    query += title + '", "'
    query += str(duration) + '", "'
    query += str(dateReleased) + '", "'
    query += str(dayRank) + '", "'
    query += str(monthRank) + '", "'
    query += str(weekRank) + '", "'
    query += str(dislikes) + '", "'
    query += str(likes) + '", "'
    query += str(artistUsername) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Update a song's attribute
@songs.route('/songs/row/<row>', methods=['PUT'])
def update_song(songID):
    cursor = db.get_db().cursor()
    cursor.execute('update Song set where songID = {0}'.format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete song from the app
@songs.route('/songs/deleted', methods=['DELETE'])
def delete_song(songID):
    cursor = db.get_db().cursor()
    cursor.execute('delete from Song where songID = {0}'.format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
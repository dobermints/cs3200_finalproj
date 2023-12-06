from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

songs = Blueprint('songs', __name__)

# Get song based on songID
@songs.route('/songs/songid/<songID>', methods=['GET'])
def get_song(songID):
    cursor = db.get_db().cursor()
    cursor.execute("select * from Song where songID = '{0}'".format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get song based on its name/title
@songs.route('/songs/<title>', methods=['GET'])
def get_song_by_title(title):
    cursor = db.get_db().cursor()
    cursor.execute("select * from Song where title LIKE '%{0}%'".format(title))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# update existing song's genre, language, or title details based on songID
@songs.route('/songs/songid/<songID>', methods=['PUT'])
def limited_update_song(songID):
    cursor = db.get_db().cursor()
    the_data = request.json
    current_app.logger.info(the_data)
    
    # grab songId and previous unchangeable details
    songInfo = get_song(songID)

    prevGenre = songInfo['genre']
    prevLanguage = songInfo['language']
    prevTitle = songInfo['title']
    
    # chaneable details
    genre = the_data['genre']
    language = the_data['language']
    title = the_data['title']
    
    query = 'UPDATE Song SET '
    query += 'genre = "' + str(genre) + '", '
    query += 'language = "' + str(language) + '", '
    query += 'title = "' + str(title) + '" '
    query += 'WHERE songID = {0};'.format(songID)

    cursor.execute(query)
    current_app.logger.info(query)
    
    db.get_db().commit()
    return 'Success!'

# Delete a song from the app by songID
@songs.route('/songs/songid/<songID>', methods=['DELETE'])
def delete_song(songID):

    query = '''
        DELETE
        FROM Song
        WHERE songID = {0};
    '''.format(songID)
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get all songs in database
@songs.route('/songs', methods=['GET'])
def get_all_songs():
    cursor = db.get_db().cursor()
    cursor.execute('select * from Song;')
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
@songs.route('/songs', methods=['POST'])
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
    query += '"' + str(songID) + '", '
    query += '"' + genre + '", '
    query += '"' + language + '", '
    query += '"' + title + '", '
    query += '"' + str(duration) + '", '
    query += '"' + str(dateReleased) + '", '
    query += '"' + str(dayRank) + '", '
    query += '"' + str(monthRank) + '", '
    query += '"' + str(weekRank) + '", '
    query += '"' + str(dislikes) + '", '
    query += '"' + str(likes) + '", '
    query += '"' + str(artistUsername) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get all songs and their likes
@songs.route('/songs/likes', methods=['GET'])
def get_all_song_likes():
    cursor = db.get_db().cursor()
    cursor.execute('select songID, title, likes from Song;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get a specific song and its number of likes
@songs.route('/songs/likes/<title>', methods=['GET'])
def get_one_song_likes(title):
    cursor = db.get_db().cursor()
    cursor.execute("select title, likes from Song where title LIKE '%{0}%'".format(" ".join(title.split("+"))))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Toggle a like to a specific song
@songs.route('/songs/likes', methods=['PUT'])
def toggle_song_likes():
    cursor = db.get_db().cursor()
    
    the_data = request.json
    current_app.logger.info(the_data)
    
    songID = the_data['songID']
    userUsername = the_data['userUsername']
    
    # grab songId and previous unchangeable details
    cursor.execute("SELECT likes FROM Song WHERE songID = '" + songID + "';")
    prev_likes = cursor.fetchall()
    prev_likes = str(prev_likes).replace(",", "").replace("(", "").replace(")","")
    query_to_check_if_liked = "SELECT count(*) FROM SongLikes WHERE songID = '" + songID + "' AND userUsername = '" + userUsername + "';"
    
    cursor.execute(query_to_check_if_liked)
    theData = cursor.fetchall()
    theData = str(theData).replace(",", "").replace("(", "").replace(")","")
    
    if theData == '0': # not liked yet
        querySong = 'UPDATE Song SET '
        querySong += "likes = " + str(int(prev_likes) + 1) + " "
        querySong += "WHERE songID = {0};".format(songID)
        
        querySongLikes = 'INSERT INTO SongLikes (songID, userUsername) VALUES ('
        querySongLikes += "'" + str(songID) + "', "
        querySongLikes += "'" + str(userUsername) + "');"
        
    elif theData == '1': # already liked song being unliked
        querySong = 'UPDATE Song SET '
        querySong += "likes = " + str(int(prev_likes) - 1) + " "
        querySong += "WHERE songID = {0};".format(songID)
        
        querySongLikes = 'DELETE FROM SongLikes WHERE '
        querySongLikes += "songID = '" + str(songID) + "' AND "
        querySongLikes += "userUsername = '" + str(userUsername) + "';"
        
    else:
        raise Exception(prev_likes + theData)
    
    cursor.execute(querySong)
    cursor.execute(querySongLikes)
    current_app.logger.info(querySong)
    current_app.logger.info(querySongLikes)

    db.get_db().commit()
    return 'Successful update with ' + prev_likes + " " + theData

# Get a specific song and its number of dislikes
@songs.route('/songs/dislikes/<songID>', methods=['GET'])
def get_one_song_dislikes(songID):
    cursor = db.get_db().cursor()
    cursor.execute('select title, dislikes from Song where songID = {0}'.format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# DO NOT USE, WE HAVE NOT CREATED A SongDislikes TABLE BUT THE PROCESS IS THE SAME AS toggle_song_likes
# Toggle a dislike to a specific song
@songs.route('/songs/dislikes', methods=['PUT'])
def toggle_song_dislikes():
    cursor = db.get_db().cursor()
    
    the_data = request.json
    current_app.logger.info(the_data)
    
    songID = the_data['songID']
    userUsername = the_data['userUsername']
    
    songInfo = get_song(songID)
    
    query_to_check_if_disliked = 'SELECT count(*) FROM SongDislikes WHERE songID = ' + songID + ' AND userUsername = ' + userUsername + ";"
    
    if query_to_check_if_disliked == 0: # not disliked yet
        
        prev_dislikes = songInfo['dislikes']
    
        querySong = 'UPDATE Song SET '
        querySong += 'dislikes = "' + str(prev_dislikes + 1) + '" '
        querySong += 'WHERE songID = {0};'.format(songID)
        
        querySongDislikes = 'INSERT INTO SongDislikes (songID, userUsername) VALUES ('
        querySongDislikes += '"' + str(songID) + '", '
        querySongDislikes += '"' + str(userUsername) + '");'
        
    elif query_to_check_if_disliked == 1: # already disliked song being un-disliked
        
        querySong = 'UPDATE Song SET '
        querySong += 'dislikes = "' + str(prev_dislikes - 1) + '" '
        querySong += 'WHERE songID = {0};'.format(songID)
        
        querySongDislikes = 'DELETE FROM SongDislikes WHERE'
        querySongDislikes += 'songID = "' + str(songID) + '" AND '
        querySongDislikes += 'userUsername = "' + str(userUsername) + '");'
        
    else:
        raise Exception('Error updating dislikes')
    
    cursor.execute(querySong)
    cursor.execute(querySongDislikes)
    current_app.logger.info(querySong)
    current_app.logger.info(querySongDislikes)

    db.get_db().commit()
    return 'Successful update'

# Update the genre attribute for a particular song
@songs.route('/songs/genre', methods=['PUT'])
def genre_update_song():
    cursor = db.get_db().cursor()
    the_data = request.json
    current_app.logger.info(the_data)
    
    genre = the_data['genre']
    songID = the_data['songID']
    
    query = 'UPDATE Song SET '
    query += 'genre = "' + str(genre) + '" '
    query += 'WHERE songID = {0};'.format(songID)

    cursor.execute(query)
    current_app.logger.info(query)
    
    db.get_db().commit()
    return 'Successful update'

# Get song rank based off title
@songs.route('/songs/rank/<title>', methods=['GET'])
def get_song_rank(title):
    cursor = db.get_db().cursor()
    cursor.execute("select title, dayRank, monthRank, weekRank from Song where title LIKE '%{0}%'".format(title))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns all liked songs by a user
@songs.route('/songs/songLikes/<username>', methods=['GET'])
def get_liked_songs(username):
    cursor = db.get_db().cursor()
    cursor.execute('select * from Song JOIN (SELECT * FROM SongLikes where userUsername = {0}'.format(username) + ") AS a ON Song.SongID = a.SongID")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
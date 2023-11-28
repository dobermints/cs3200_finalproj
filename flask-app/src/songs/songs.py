from flask import Blueprint, request, jsonify, make_response
import json
from src import db

songs = Blueprint('songs', __name__)

# Get song rank for specific song by SongID 
@songs.route('/songs/<rank>', methods=['GET'])
def get_song_rank(songID):
    cursor = db.get_db().cursor()
    cursor.execute('select rank from songs where songID = {0}'.format(songID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
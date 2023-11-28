from flask import Blueprint, request, jsonify, make_response
import json
from src import db

artists = Blueprint('artists', __name__)

# Get artist rank for artist with 
@artists.route('/artists/<rank>', methods=['GET'])
def get_artist_rank(username):
    cursor = db.get_db().cursor()
    cursor.execute('select rank from customers where username = {0}'.format(username))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
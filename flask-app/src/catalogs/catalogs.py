from flask import Blueprint, request, jsonify, make_response
import json
from src import db


catalogs = Blueprint('catalogs', __name__)

# Get catalog detail for catalog with particular catalogID
@catalogs.route('/Catalog/<catalogID>', methods=['GET'])
def get_catalog(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from catalogs where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add new catalog
@catalogs.route('/Catalog/<catalogID>', methods=['POST'])
def get_customer(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('insert into catalogs values (catalogID = ' + str({0}.format(catalogID)) + ')')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update catalog detail for catalog with particular catalogID
@catalogs.route('/Catalog/<catalogID>', methods=['PUT'])
def get_customer(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('update * from catalogs where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete catalog detail for catalog with particular catalogID
@catalogs.route('/Catalog/<catalogID>', methods=['DELETE'])
def get_customer(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('delete from catalogs where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

catalogs = Blueprint('catalogs', __name__)

# Get catalog based on catalogID
@catalogs.route('/catalogs/<catalogID>', methods=['GET'])
def get_catalog(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from SongCatalog where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Create/make public catalog
@catalogs.route('/catalog', methods=['POST'])
def create_catalog_listing():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    catalogID = the_data['catalogID']
    totalSales = the_data['total_sales']
    value = the_data['value']
    genre = the_data['genre']
    name = the_data['name']
    companyID = the_data['companyID']
    songID = the_data['songID']

    # Constructing the query
    query = 'insert into SongCatalog (catalogID, totalSales, value, genre, name, companyID, songID) values ("'
    query += str(catalogID) + '", "'
    query += str(totalSales) + '", "'
    query += str(value) + '", '
    query += genre + '", "'
    query += name + '", "'
    query += str(companyID) + '", '
    query += str(songID) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Update a song catalog
@catalogs.route('/catalog/row/<row>', methods=['PUT'])
def update_catalog_listing(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('update SongCatalog set where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete catalog for a specific catalogID
@catalogs.route('/catalog/deleted', methods=['DELETE'])
def delete_catalog_listing(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('delete from SongCatalog where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
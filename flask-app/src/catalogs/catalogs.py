from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

catalogs = Blueprint('catalogs', __name__)

# Create/make public catalog
@catalogs.route('/catalogs', methods=['POST'])
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
    query = 'insert into SongCatalog (catalogID, totalSales, value, genre, name, companyID, songID) values ('
    query += "'" + str(catalogID) + "', "
    query += str(totalSales) + ", "
    query += str(value) + ", "
    query += "'" + genre + "', "
    query += "'" + name + "', "
    query += "'" + str(companyID) + "', "
    query += "'" + str(songID) + "')"
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

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

# Update a song catalog
@catalogs.route('/catalogs/<catalogID>', methods=['PUT'])
def update_catalog_listing(catalogID):
    cursor = db.get_db().cursor()
    the_data = request.json
    current_app.logger.info(the_data)
    
    totalSales = the_data['totalSales']
    value = the_data['value']
    genre = the_data['genre']
    name = the_data['name']
    
    query = 'update SongCatalog set'
    query += 'totalSales = "' + str(totalSales) + '", '
    query += 'value = "' + str(value) + '", '
    query += 'genre = "' + str(genre) + '", '
    query += 'name = "' + str(name) + '" '
    query += 'where catalogID = {0};'.format(catalogID)

    cursor.execute(query)
    current_app.logger.info(query)
    db.get_db().commit()
    
    return 'Success!'

# Delete catalog for a specific catalogID
@catalogs.route('/catalogs/<catalogID>', methods=['DELETE'])
def delete_catalog_listing(catalogID):
    cursor = db.get_db().cursor()
    
    query = 'delete from SongCatalog where catalogID = {0};'.format(catalogID)
    cursor.execute(query)
    current_app.logger.info(query)
    db.get_db().commit()
    
    return 'Success!'

# Get catalog based on genre
@catalogs.route('/catalogs/catalog-genre/<genre>', methods=['GET'])
def filter_catalog_by_genre(genre):
    cursor = db.get_db().cursor()
    cursor.execute('select * from SongCatalog where genre = {0}'.format(genre))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the genre of a particular catalog
@catalogs.route('/catalogs/genre/<catalogID>', methods=['GET'])
def get_genre_of_catalog(catalogID):
    cursor = db.get_db().cursor()
    cursor.execute('select genre from SongCatalog where catalogID = {0}'.format(catalogID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
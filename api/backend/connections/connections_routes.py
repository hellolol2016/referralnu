from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

connections = Blueprint('Connections', __name__)

# Get all connections
@connections.route("/", methods=["GET"])
def get_all_connections():
    query = '''
        SELECT connectionId,
               studentId,
               referrerId,
               creationDate
        FROM Connections
        ORDER BY creationDate
    '''

    current_app.logger.info(f'GET / query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({'error fetching connections': str(e)}))
        res.status_code = 500
    return res

@connections.route("/<studentId>", methods=["GET"])
def get_connections_by_studentId(studentId):

    query = '''
    SELECT connectionId,
           studentId,
           referrerId,
           creationDate
    FROM Connections
    WHERE studentId = %s
    ORDER BY creationDate;
    '''

    current_app.logger.info(f'GET /<studentId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching requests by referrer": str(e)}))
        res.status_code = 500
    return res

# Create a new connection
@connections.route("/", methods=["POST"])
def create_connection():
    try:
        body = request.get_json()
        studentId = body['studentId']
        referrerId = body['referrerId']

        query = '''
            INSERT INTO Connections (studentId, referrerId, creationDate)
            VALUES (%s, %s, NOW())
        '''

        current_app.logger.info(f'POST /connections query: {query}')
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId, referrerId,))
        res = make_response(jsonify({"message": "Connection created"}))
        res.status_code = 201
    except Exception as e:
        res = make_response(jsonify({'error creating connection': str(e)}))
        res.status_code = 500
    return res


# Delete connections
@connections.route("/<connectionId>", methods=["DELETE"])
def delete_connections(connectionId):
    try:
        #body = request.get_json()
        #connectionId = body.get('connectionId')

        #if not connectionId:
            #return make_response(jsonify({"error": "Missing connectionId"}), 400)

        query = '''
            DELETE FROM Connections
            WHERE connectionId = %s
        '''

        current_app.logger.info(f'DELETE /connections query: {query}')

        cursor = db.get_db().cursor()
        cursor.execute(query, (connectionId,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            res = make_response(jsonify({"message": "No connections found"}), 404)
        else:
            res = make_response(jsonify({"message": "Connection deleted"}))
            res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({'error deleting connection': str(e)}))
        res.status_code = 500
    return res
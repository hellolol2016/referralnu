from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

connections = Blueprint('connections', __name__)

# Get all connections
@connections.route("/", methods=["GET"])
def get_all_connections():
    query = '''
        SELECT connectionId,
               studentId,
               referrerId,
               company,
               status,
               createdAt
        FROM connections
        ORDER BY createdAt
    '''

    current_app.logger.info(f'GET /connections query: {query}')

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


# Create a new connection
@connections.route("/", methods=["POST"])
def create_connection():
    try:
        body = request.get_json()
        studentId = body['studentId']
        referrerId = body['referrerId']
        company = body.get('company', None)
        status = body.get('status', 'Pending')

        query = '''
            INSERT INTO connections (studentId, referrerId, company, status, createdAt)
            VALUES (%s, %s, %s, %s, NOW())
        '''

        current_app.logger.info(f'POST /connections query: {query}')
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId, referrerId, company, status))
        res = make_response(jsonify({"message": "Connection created"}))
        res.status_code = 201
    except Exception as e:
        res = make_response(jsonify({'error creating connection': str(e)}))
        res.status_code = 500
    return res


# Delete multiple connections
@connections.route("/", methods=["DELETE"])
def delete_connections():
    try:
        body = request.get_json()
        connectionIds = body['connectionIds']

        query = '''
            DELETE FROM Connections
            WHERE connectionId IN (%s)
        ''' % ','.join(['%s'] * len(connectionIds))
        current_app.logger.info(f'DELETE /connections query: {query}')

        cursor = db.get_db().cursor()
        cursor.execute(query, connectionIds)
        db.get_db().commit()
        res = make_response(jsonify({"message": f"Deleted {cursor.rowcount} connections successfully"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error deleting connections": str(e)}))
        res.status_code = 500
    return res
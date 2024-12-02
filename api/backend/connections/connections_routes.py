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



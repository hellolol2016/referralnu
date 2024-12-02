from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

advisor = Blueprint('advisor', __name__)

# Get advisor info
@advisor.route("/advisor/<advisorID>", methods=['GET'])
def get_advisor_information(advisorID):
    query = '''
        SELECT advisorId,
               firstName,
               lastName,
               email,
               phoneNumber,
               college
        FROM Advisors
        WHERE advisorId = %s
    '''

    current_app.logger.info(f'GET /advisor/<advisorId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (advisorID,))
        data = cursor.fetchall()

        if not data:
            res = make_response(jsonify({'error': 'No advisor found'}))
            res.status_code = 404
        else:
            res = make_response(jsonify({'advisor': data}))
            res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({'error': str(e)}))
        res.status_code = 500

    return res

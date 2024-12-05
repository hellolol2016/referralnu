from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db
from datetime import datetime, timedelta

advisor = Blueprint('advisor', __name__)

# Get advisor info
@advisor.route("/<advisorID>", methods=['GET'])
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

    current_app.logger.info(f'GET /<advisorId> query: {query}')

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


# Set reminder for follow-up communication
@advisor.route("/set_reminder/<studentId>/<advisorId>", methods=['POST'])
def set_reminder(studentId,advisorId):
    request_data = request.get_json()
    content = request_data.get('content')
    follow_up_days = request_data.get('followUpDays', 3) 

    follow_up_date = datetime.now() + timedelta(days=follow_up_days)

    query = '''
        INSERT INTO Advisor_Messages (
            studentId, advisorId, content, followUpDate, reminderStatus
        ) VALUES (%s, %s, %s, %s, 'pending')
    '''

    current_app.logger.info(f"POST /set_reminder query: {query} with data: "
                            f"{studentId}, {advisorId}, {content}, {follow_up_date}")

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId, advisorId, content, follow_up_date))
        db.get_db().commit()

        res = make_response(jsonify({
            'message': 'Reminder set successfully',
            'followUpDate': follow_up_date.strftime('%Y-%m-%d %H:%M:%S')
        }))
        res.status_code = 201
    except Exception as e:
        current_app.logger.error(f"Error in POST /set_reminder: {str(e)}")
        res = make_response(jsonify({'error': str(e)}))
        res.status_code = 500

    return res


from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db
from datetime import datetime

students = Blueprint('Students', __name__)

@students.route('/students/<advisorId>', methods = ['GET'])
def get_students_by_advisor(advisorId):

    query = '''
        SELECT s.studentId,
        SUM(req.pendingStatus = 'Pending') AS pendingRequests,
        SUM(req.pendingStatus = 'Accepted') AS acceptedRequests,
        SUM(req.pendingStatus = 'Rejected') AS rejectedRequests
        FROM Students s
        LEFT JOIN Requests req ON s.studentId = req.studentId
        WHERE s.advisorId = %s
        GROUP BY s.studentId
    '''

    current_app.logger.info(f'GET /students/<advisorId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (advisorId,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching requests by advisor": str(e)}))
        res.status_code = 500
    return res


@students.route('/students/<advisorId>', methods=['PUT'])
def update_or_remove_advisor(advisorId):
    try:
        # Get the request data (newAdvisorId)
        req = request.json
        new_advisor_id = req.get("newAdvisorId")

        # If newAdvisorId is not provided, we want to remove the advisor
        if new_advisor_id is None:
            # Remove advisor (set advisorId to NULL for all students with the current advisor)
            update_query = '''
                UPDATE Students
                SET advisorId = NULL
                WHERE advisorId = %s;
            '''
            cursor = db.get_db().cursor()
            cursor.execute(update_query, (advisorId,))

            # Commit the changes
            db.get_db().commit()
            return make_response(jsonify({"message": "Advisor removed successfully from students"}), 200)

        # Otherwise, we update the advisor to the new one
        else:
            update_query = '''
                UPDATE Students
                SET advisorId = %s
                WHERE advisorId = %s;
            '''
            cursor = db.get_db().cursor()
            cursor.execute(update_query, (new_advisor_id, advisorId))

            # Commit the changes
            db.get_db().commit()
            return make_response(jsonify({"message": "Advisor updated successfully for students"}), 200)

    except Exception as e:
        # Log the error and return a failure response
        current_app.logger.error(f"Error updating/removing advisor: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)



@students.route('/students/<studentId>', methods = ['GET'])
def get_results_by_student(studentId):


    query = '''
        SELECT s.StudentId, s.firstName, s.lastName, r.createdAt, r.pendingStatus
        FROM Students s JOIN Advisor a ON s.advisorId = a.advisorId
        JOIN Requests r ON s.StudentId = r.StudentId
        WHERE studentId = {studentId}
    '''

    current_app.logger.info(f'GET /students/<advisorId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching requests by student": str(e)}))
        res.status_code = 500
    return res

@students.route('/students/<studentId>', methods = ['POST'])
def send_message(studentId):
    req = request.json
    current_app.logger.info(req)

    advisorId = req.get("advisorId")
    content = req.get("content")

    
    query = '''
        INSERT INTO Advisor_Messages (content, advisorId, studentId)
        VALUES ('{content}', {advisorId}, {studentId})
    '''

    current_app.logger.info(f'POST /students/<studentId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (content, advisorId, studentId))
        db.get_db().commit()

        res = make_response(jsonify({"message": f"Updated successful"}))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error updating student details: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@students.route('/students/<studentId>', methods = ['DELETE'])
def delete_student(studentId):
    req = request.json
    current_app.logger.info(req)


    query = '''
        DELETE FROM Students WHERE studentId = {studentId};
    '''

    current_app.logger.info(f'DELETE /students/<studentId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId))
        db.get_db().commit()

        res = make_response(jsonify({"message": f"Updated successful"}))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error updating student details: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@students.route('/students/<studentId>/reminder', methods=['POST'])
def send_reminder(studentId):
    try:
        # Get current date and time
        current_time = datetime.now()

        # Query messages requiring reminders for the student
        query = f'''
            SELECT m.messageId, m.content, m.followUpDate, m.reminderStatus, s.email
            FROM Advisor_Messages m
            JOIN Students s ON m.studentId = s.studentId
            WHERE m.studentId = {studentId}
              AND m.followUpDate <= '{current_time}'
              AND m.reminderStatus = 'pending';
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query)
        reminders = cursor.fetchall()

        if not reminders:
            return make_response(jsonify({"message": "No pending reminders found"}), 200)

        # Loop through reminders and send notifications
        for reminder in reminders:
            messageId, content, followUpDate, reminderStatus, studentEmail = reminder

            # Example: Log or send reminder (replace with actual email logic)
            current_app.logger.info(f"Sending reminder to {studentEmail}: {content}")

            # Update the reminderStatus to 'sent'
            update_query = f'''
                UPDATE Advisor_Messages
                SET reminderStatus = 'sent'
                WHERE messageId = {messageId};
            '''
            cursor.execute(update_query)

        # Commit updates to the database
        db.get_db().commit()

        # Return success message
        return make_response(jsonify({"message": "Reminders sent successfully"}), 200)
    except Exception as e:
        current_app.logger.error(f"Error sending reminders: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)

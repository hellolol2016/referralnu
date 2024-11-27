
from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

messages = Blueprint('messages', __name__)


@messages.route("/<id>", methods=["DELETE"])
def delete_message(id):
    query = f'''
        DELETE FROM Messages
        WHERE id = {id}
    '''
    current_app.logger.info(f'DELETE message/<id> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        #data = cursor.fetchall()
        res = make_response(jsonify({"message": "Message deleted"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error deleting message": str(e)}))
        res.status_code = 500
    return res

@messages.route("/conversation/<referrerId>/<studentId>", methods=["GET"])
def get_conversation(referrerId, studentId):
    query = '''
      SELECT m.messageId, 
              m.messageContent, 
              m.sentAt, 
              m.studentId, 
              m.referrerId, 
              c.referrerId,
              c.studentId
      FROM Messages m
      JOIN Connections c ON m.referrerId = c.referrerId AND m.studentId = c.studentId
      WHERE c.referrerId = %s AND c.studentId = %s
      ORDER BY m.sentAt 
    '''

    current_app.logger.info(f'GET conversation/<connectionId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query,(referrerId, studentId))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching conversation": str(e)}))
        res.status_code = 500
    return res

@messages.route("/student/<studentId>", methods=["GET"])
def get_student_messages(studentId):
    query = f'''
        SELECT m.id, 
               m.messageContent, 
               m.sentAt, 
               m.senderId, 
               m.receiverId, 
               c.connectionId
        FROM Messages m
        WHERE m.senderId = {studentId}
        ORDER BY m.sentAt 
    '''
    current_app.logger.info(f'GET student/<studentId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching student messages": str(e)}))
        res.status_code = 500
    return res

@messages.route("/referrer/<referrerId>", methods=["GET"])
def get_referrer_messages(referrerId):
    query = f'''
        SELECT m.id, 
               m.messageContent, 
               m.sentAt, 
               m.senderId, 
               m.receiverId, 
               c.connectionId
        FROM Messages m
        WHERE m.senderId = {referrerId}
        ORDER BY m.sentAt 
    '''
    current_app.logger.info(f'GET referrer/<referrerId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching referrer messages": str(e)}))
        res.status_code = 500
    return res
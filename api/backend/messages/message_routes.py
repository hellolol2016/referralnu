
from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

messages = Blueprint('messages', __name__)


@messages.route("/<messageId>", methods=["DELETE"])
def delete_message(messageId):
    query = f'''
        DELETE FROM Messages
        WHERE messageId = {messageId}
    '''
    current_app.logger.info(f'DELETE message/<messageId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        #data = cursor.fetchall()
        res = make_response(jsonify({"message": "Message deleted"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error deleting message": str(e)}))
        res.status_code = 500
    return res

@messages.route("/conversation/<referrerId>/<studentId>", methods=["POST"])
def add_message(referrerId, studentId):
    req = request.json
    current_app.logger.info(req)

    messageContent = req.get("messageContent")
    adminId = req.get("adminId", 1)
    connectionId = req.get("connectionId")
    studentSent = req.get("studentSent", False)
    query = f'''
        INSERT INTO Messages (messageContent, adminId, connectionId, referrerId, studentId, studentSent)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    current_app.logger.info(query)

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (messageContent, adminId, connectionId, referrerId, studentId, studentSent))
        db.get_db().commit()
        res = make_response(jsonify({"message": "Message added"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching conversation": str(e)}))
        res.status_code = 500
    return res

@messages.route("/", methods=["GET"])
def get_all_messages():
    query = '''
      SELECT * FROM Messages 
      ORDER BY sentAt 
    '''

    current_app.logger.info(f'GET conversation/<connectionId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching conversation": str(e)}))
        res.status_code = 500
    return res

@messages.route("/conversation/<connectionId>", methods=["GET"])
def get_conversation(connectionId):
    query = '''
      SELECT m.messageId, 
              m.messageContent, 
              m.sentAt, 
              m.studentId, 
              m.referrerId, 
              m.studentSent
      FROM Messages m
      WHERE m.connectionId = %s
      ORDER BY m.sentAt 
    '''

    current_app.logger.info(f'GET conversation/<connectionId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query,(connectionId))
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
        SELECT m.messageId, 
               m.messageContent, 
               m.sentAt, 
               m.referrerId, 
               m.studentId, 
               m.connectionId
        FROM Messages m
        WHERE m.studentId = {studentId}
        AND m.studentSent = true
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

@messages.route("/keyword/<keyword>", methods=["DELETE"])
def remove_bad_messages(keyword):
    query = f'''
        DELETE FROM Messages m
        WHERE LOWER(messageContent) LIKE LOWER(%s)
    '''
    current_app.logger.info(f'DELETE /<keyword> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (f'%{keyword}%'))
        db.get_db().commit()
        rows_deleted = cursor.rowcount
        res = make_response(jsonify({"message": f"Removed all {rows_deleted} messages with keyword: {keyword}"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching referrer messages": str(e)}))
        res.status_code = 500
    return res

@messages.route("/referrer/<referrerId>", methods=["GET"])
def get_referrer_messages(referrerId):
    query = f'''
        SELECT m.messageId, 
               m.messageContent, 
               m.sentAt, 
               m.referrerId, 
               m.studentId, 
               m.connectionId
        FROM Messages m
        WHERE m.referrerId = {referrerId}
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

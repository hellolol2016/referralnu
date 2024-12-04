# 4.5

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

@requests.route("/", methods=["GET"])
def get_requests():

    query = '''
        SELECT Req.requestId, 
        Req.pendingStatus, 
        Req.requestDate, 
        Req.createdAt, 
        Req.lastViewed, 
        Com.name, 
        Mes.messageContent, 
        Mes.sentAt
        FROM Requests Req
        LEFT JOIN Messages Mes 
        ON Req.studentId = Mes.studentId 
        AND Req.requestId = Mes.connectionId
        JOIN Companies Com 
        ON Req.companyId = Com.companyId
        ORDER BY Req.requestDate DESC;
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res
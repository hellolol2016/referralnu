from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

@requests.route("/requests", methods=["GET"])
def get_requests():

    query = '''
        SELECT Req.requestId, 
        Req.companyName, 
        Req.pendingStatus, 
        Req.requestDate, 
        Req.createdAt, 
        Req.lastViewed, 
        Com.name, 
        Mes.messageContent, 
        Mes.sentAt
        FROM Requests Req
        LEFT JOIN Messages Mes 
        ON Req.studentId = M.studentId 
        AND Req.requestId = Mess.connectionId
        JOIN Company Com 
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

@requests.route("/requests", methods=["POST"])
def create_request():

    req = request.json
    current_app.logger.info(req)

    # Extract and validate required fields
    studentId = req.get("studentId")
    adminId = req.get("adminId")

    # Optional fields
    description = req.get("description", "")
    # Default status is "Pending"?
    status = req.get("status", "Pending")

    query = f"""
        INSERT INTO Requests (studentId, adminId, description, status)
        VALUES ({studentId}, {adminId}, '{description}', '{status}')
    """

    current_app.logger.info(query)

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        res = make_response(jsonify({"message": "Request created successfully"}))
        res.status_code = 201
    except Exception as e:
        current_app.logger.error(f"Error creating request: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/requests", methods=["DELETE"])
def delete_requests():
    try:
        body = request.get_json()
        requestIds = body['requestIds']

        query = '''
            DELETE FROM Requests
            WHERE requestId IN (%s)
        ''' % ','.join(['%s'] * len(requestIds))
        current_app.logger.info(f'DELETE /requests query: {query}')

        cursor = db.get_db().cursor()
        cursor.execute(query, requestIds)
        db.get_db().commit()
        res = make_response(jsonify({"message": f"Deleted {cursor.rowcount} requests successfully"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error deleting requests": str(e)}))
        res.status_code = 500
    return res

@requests.route("/requests/<requestId>", methods=["GET"])
def get_requests():

    query = '''
        SELECT Req.requestId, 
        Req.companyName, 
        Req.pendingStatus, 
        Req.requestDate, 
        Req.createdAt, 
        Req.lastViewed, 
        FROM Requests Req
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
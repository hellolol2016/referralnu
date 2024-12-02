from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

@requests.route("/requests", methods=["GET"])
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

@requests.route("/requests/<int:requestId>", methods=["DELETE"])
def delete_request(requestId):
    try:
        query = '''
            DELETE FROM Requests
            WHERE requestId = %s
        '''
        current_app.logger.info(f'DELETE /requests query: {query}')

        cursor = db.get_db().cursor()
        cursor.execute(query, requestId)
        db.get_db().commit()
        res = make_response(jsonify({"message": "Request deleted successfully"}))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error deleting requests": str(e)}))
        res.status_code = 500
    return res

@requests.route("/requests/referrer/<referrerId>", methods=["GET"])
def get_requests_by_referrer(referrerId):

    query = '''
        SELECT C.studentId, 
        S.name AS studentName, 
        R.company AS referredCompany, 
        C.creationDate AS referralDate, 
        Req.status AS applicationStatus
        FROM Connections C
        JOIN Referrer R 
        ON C.referrerId = R.referrerId
        JOIN Students S 
        ON C.studentId = S.studentId
        JOIN Requests Req 
        ON Req.studentId = S.studentId 
        AND Req.referrerId = R.referrerId
    '''

    current_app.logger.info(f'GET /requests/referrer/<referrerId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (referrerId))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching requests by referrer": str(e)}))
        res.status_code = 500
    return res

@requests.route("/requests/<requestId>", methods=["GET"])
def get_referral_request_info():

    query = '''
        SELECT Req.requestId, 
        Com.name, 
        Req.pendingStatus, 
        Req.requestDate, 
        Req.createdAt, 
        Req.lastViewed, 
        FROM Requests Req
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

@requests.route("/requests/<requestId>", methods=["POST"])
def create_connections():

    req = request.json
    current_app.logger.info(req)

    studentId = req.get("studentId")
    referralId = req.get("referralId")

    query = f"""
        INSERT INTO Connections (referralId, studentId)
        VALUES ({referralId}, {studentId})
    """

    current_app.logger.info(query)

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        res = make_response(jsonify({"message": "Connection created successfully"}))
        res.status_code = 201
    except Exception as e:
        current_app.logger.error(f"Error creating connection: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/requests/<requestId>", methods=["PUT"])
def update_request_status():

    req = request.json
    current_app.logger.info(req)

    status = req.get("status")
    requestId = req.get("requestId")

    query = """
        UPDATE Requests
        SET status = {status}
        WHERE requestId = {requestId}
    """

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (status, requestId))
        db.get_db().commit()

        res = make_response(jsonify({"message": f"Request status updated to '{status}' successfully"}))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error updating request status: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/requests/company/<companyId>", methods=["GET"])
def get_request_company():

    query = '''
        SELECT S.studentId, S.name AS studentName, S.contactInfo AS studentContact, R.company AS referredCompany, C.creationDate AS referralDate
        FROM Connections C
        JOIN Referrer R ON C.referrerId = R.referrerId
        JOIN Students S ON C.studentId = S.studentId
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

# @requests.route("/requests/<referrerId>", methods=["PUT"])
# def update_request_status(referrerId):

#     req = request.json
#     current_app.logger.info(req)

#     requestId = req.get("requestId", [])
#     status = req.get("status")

#     query = """
#         UPDATE Requests
#         SET status = %s
#         WHERE requestId IN (%s) AND referrerId = %s
#     """ % (', '.join(['%s'] * len(requestId)))

#     current_app.logger.info(f'PUT /requests/<referrerId> query: {query}')

#     try:
#         cursor = db.get_db().cursor()
#         cursor.execute(query, (status, requestId, referrerId))
#         db.get_db().commit()

#         res = make_response(jsonify({"message": f"Updated successful"}))
#         res.status_code = 200
#     except Exception as e:
#         current_app.logger.error(f"Error updating referrer details: {str(e)}")
#         res = make_response(jsonify({"error": str(e)}))
#         res.status_code = 500

#     return res

@requests.route("/requests/<studentId>", methods=["GET"])
def get_student_requests(studentId):
    query = """
            SELECT S.studentId, 
            S.name AS studentName, 
            S.contactInfo AS studentContact, 
            R.company AS referredCompany, 
            C.creationDate AS referralDate
            FROM Connections C
            JOIN Referrer R ON C.referrerId = R.referrerId
            JOIN Students S ON C.studentId = S.studentId
            WHERE r.studentId = %s
        """

    current_app.logger.info(f"GET /requests/{studentId} query: {query}")

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

@requests.route("/requests/<status>", methods=["GET"])
def get_requests_by_status(status):
    query = """
        SELECT 
            r.requestId, 
            r.studentId, 
            r.referrerId, 
            r.status, 
            r.submissionDate, 
            s.name AS studentName, 
            ref.name AS referrerName
        FROM Requests r
        JOIN Students s ON r.studentId = s.studentId
        JOIN Referrers ref ON r.referrerId = ref.referrerId
        WHERE r.status = %s
    """
    current_app.logger.info(f"GET /requests/{status} query: {query}")

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
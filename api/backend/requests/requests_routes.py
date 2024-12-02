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

@requests.route("/info", methods=["POST"])
def create_request():

    req = request.json
    current_app.logger.info(req)

    # Extract and validate required fields
    studentId = req.get("studentId")
    # Default status is "Pending"?
    pendingStatus = req.get("pendingStatus", "Pending")

    companyId = req.get("companyId")
    
    query = f"""
        INSERT INTO Requests (studentId, pendingStatus, companyId)
        VALUES ({studentId}, '{pendingStatus}', {companyId})
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

@requests.route("/<requestId>", methods=["DELETE"])
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

@requests.route("/referrer/<referrerId>", methods=["GET"])
def get_requests_by_referrer(referrerId):

    query = '''
    SELECT 
        C.studentId, 
        S.firstName, 
        S.lastName, 
        R.companyId AS referredCompany, 
        C.creationDate AS referralDate, 
        Req.pendingStatus AS applicationStatus
    FROM Connections C
    JOIN Referrers R 
        ON C.referrerId = R.referrerId
    JOIN Students S 
        ON C.studentId = S.studentId
    JOIN Requests Req 
        ON Req.studentId = S.studentId 
        AND Req.companyId = R.companyId
    WHERE Req.requestId = %s;
    '''

    current_app.logger.info(f'GET /referrer/<referrerId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (referrerId,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error fetching requests by referrer": str(e)}))
        res.status_code = 500
    return res

@requests.route("/referral/<requestId>", methods=["GET"])
def get_referral_request_info(requestId):

    query = '''
        SELECT 
        Req.requestId, 
        Com.name, 
        Req.pendingStatus, 
        Req.requestDate, 
        Req.createdAt, 
        Req.lastViewed 
        FROM Requests Req
        JOIN Companies Com 
        ON Req.companyId = Com.companyId
        WHERE Req.requestId = %s
        ORDER BY Req.requestDate DESC; 
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (requestId,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/connections/<requestId>", methods=["POST"])
def create_connections(requestId):

    req = request.json
    current_app.logger.info(req)

    studentId = req.get("studentId")
    referrerId = req.get("referrerId")

    query = f"""
        INSERT INTO Connections (referrerId, studentId)
        VALUES ({referrerId}, {studentId})
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

@requests.route("/status/<int:requestId>", methods=["PUT"])
def update_request_status(requestId):
    req = request.json
    current_app.logger.info(req)

    pendingStatus = req.get("pendingStatus", "pending")

    query = """
        UPDATE Requests
        SET pendingStatus = %s
        WHERE requestId = %s
    """

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (pendingStatus, requestId))
        db.get_db().commit()

        res = make_response(jsonify({"message": f"Request status updated to '{pendingStatus}' successfully"}))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error updating request status: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/company/<companyId>", methods=["GET"])
def get_request_company(companyId):

    query = '''
        SELECT S.studentId, S.firstName, S.lastName, S.phoneNumber, S.email, R.companyId AS referredCompany, C.creationDate AS referralDate
        FROM Connections C
        JOIN Referrers R ON C.referrerId = R.referrerId
        JOIN Students S ON C.studentId = S.studentId
        WHERE R.companyId = %s
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (companyId,))
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

@requests.route("/student/<studentId>", methods=["GET"])
def get_student_requests(studentId):
    query = """
            SELECT S.studentId, 
            S.firstName,
            S.lastName, 
            S.phoneNumber,
            S.email,
            R.companyId AS referredCompany, 
            C.creationDate AS referralDate
            FROM Connections C
            JOIN Referrers R ON C.referrerId = R.referrerId
            JOIN Students S ON C.studentId = S.studentId
            WHERE S.studentId = %s
        """

    current_app.logger.info(f"GET /student/{studentId} query: {query}")

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (studentId,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/<status>", methods=["GET"])
def get_requests_by_status(status):
    query = """
        SELECT 
            r.requestId, 
            r.studentId, 
            r.companyId, 
            r.pendingStatus, 
            r.requestDate, 
            s.firstName, 
            s.lastName,
            ref.name AS referrerName
        FROM Requests r
        JOIN Students s ON r.studentId = s.studentId
        JOIN Referrers ref ON r.companyId = ref.companyId
        WHERE r.pendingStatus = %s
    """
    current_app.logger.info(f"GET /{status} query: {query}")

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (status,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res
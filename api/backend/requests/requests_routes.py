
from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

@requests.route("/", methods=["GET"])
def get_requests():

    query = '''
        SELECT * 
        FROM Requests;
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
        Req.createdAt, 
        Req.lastViewed 
        FROM Requests Req
        JOIN Companies Com 
        ON Req.companyId = Com.companyId
        WHERE Req.requestId = %s
        ORDER BY Req.createdAt DESC; 
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
            r.createdAt, 
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

@requests.route("/referrer/<int:referrerId>", methods=["PUT"])
def update_referrer_info(referrerId):
    req = request.json
    current_app.logger.info(req)

    name = req.get("name")
    email = req.get("email")
    phoneNumber = req.get("phoneNumber")

    query = """
        UPDATE Referrers
        SET name = %s, email = %s, phoneNumber = %s
        WHERE referrerId = %s
    """

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (name, email, phoneNumber, referrerId))
        db.get_db().commit()

        res = make_response(jsonify({"message": "Referrer information updated successfully"}))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error updating referrer information: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@requests.route("/student/<student_id>", methods=["GET"])
def get_requests_by_student(student_id):
    query = """
        SELECT 
            r.requestId,
            r.studentId,
            r.pendingStatus,
            r.companyId,
            r.createdAt,
            r.lastViewed,
            r.viewCount,
            s.firstName,
            s.lastName,
            s.email,
            s.phoneNumber
        FROM Requests r
        WHERE r.studentId = %s
    """
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (student_id,))
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@requests.route("/<student_id>/<status>", methods=["GET"])
def get_requests_by_student_and_status(student_id, status):
    query = """
        SELECT 
            r.requestId, 
            r.studentId, 
            r.companyId, 
            r.pendingStatus, 
            r.createdAt, 
            s.firstName, 
            s.lastName,
            ref.name AS referrerName
        FROM Requests r
        JOIN Students s ON r.studentId = s.studentId
        JOIN Referrers ref ON r.companyId = ref.companyId
        WHERE r.pendingStatus = %s AND r.studentId = %s
    """
    current_app.logger.info(f"GET /{student_id}/{status} query: {query}")

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (status, student_id))  # Passing both status and student_id
        data = cursor.fetchall()

        # If no data found, return a 404 response or an empty list
        if not data:
            res = make_response(jsonify([]))  # Returning an empty list if no requests found
            res.status_code = 200
        else:
            res = make_response(jsonify(data))
            res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res



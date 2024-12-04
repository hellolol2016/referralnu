# 4.1

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

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
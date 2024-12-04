# 4.4

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

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
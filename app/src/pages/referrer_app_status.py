# 4.3

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

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
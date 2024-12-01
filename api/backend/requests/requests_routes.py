from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('requests', __name__)

# Update advisor messages with new message
@requests.route("/<pendingStatus>/advisor_messages", methods = ["PUT"])
def update_advisor_message(pendingStatus):
    try:
        req_data = request.get_json()
        new_content = req_data["content"]
        update_date = req_data["updateDate", None]

        query = '''
            UPDATE advisor_messages
            SET advisor_message = ?
            WHERE advisorId = ?'''

        params = (new_content, pendingStatus)



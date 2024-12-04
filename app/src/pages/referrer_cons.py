# 4.4

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

@requests.route("/connections/<requestId>", methods=["POST"])
def create_connections(requestId):


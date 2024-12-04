# 4.6

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

requests = Blueprint('Requests', __name__)

@referrers.route("/", methods=["POST"])
def create_referrer():

    req = request.json
    current_app.logger.info(req)

    name = req["name"]
    email = req["email"]
    #phone can be null
    phoneNumber = req.get("phoneNumber", "")
    adminId = req["adminId"]
    companyId = req["companyId"]
    #numreferrals can be null
    numreferrals = req.get("numReferrals")

    #not sure if query inserting None is ok
    query = f'''
        INSERT INTO Referrers (name, 
                               email, 
                               phoneNumber, 
                               adminId, 
                               companyId, 
                               numReferrals)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    current_app.logger.info(query)
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (name, email, phoneNumber, adminId, companyId, numreferrals))  # Pass the values here
        db.get_db().commit()
        res = make_response(jsonify({"message": "Referrer created"}))
        res.status_code = 201
    except Exception as e:
        res = make_response(jsonify({"error when creating referrer": str(e)}))
        res.status_code = 500

    return res

from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

referrers = Blueprint('referrers', __name__)


@referrers.route("/referrers", methods=["GET"])
def get_referrers():
    query = '''
        SELECT r.referrer_id, 
               r.referrer_name, 
               r.referrer_email,
               r.numReferrals,
               c.name as company_name
        FROM referrers r
        JOIN companies c ON referrers.companyId = companies.companyId
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

@referrers.route("/referrers", methods=["POST"])
def create_referrer():

    req = request.json
    current_app.logger.info(req)

    name = req["name"]
    email = req["email"]
    #phone can be null
    phone = req.get("phone", None)
    adminId = req["adminId"]
    companyId = req["companyId"]
    #numreferrals can be null
    numreferrals = req.get("numReferrals",None)

    #not sure if query inserting None is ok 
    query = f'''
        INSERT INTO referrers (referrer_name, 
                               referrer_email, 
                               referrer_phone, 
                               adminId, 
                               companyId, 
                               numReferrals)
        VALUES ('{name}', '{email}', '{phone}', {adminId}, {companyId}, {numreferrals})
    '''

    

    current_app.logger.info(query)
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        res = make_response(jsonify({"message": "Referrer created"}))
        res.status_code = 201
    except Exception as e:
        res = make_response(jsonify({"error when creating referrer": str(e)}))
        res.status_code = 500

    return res